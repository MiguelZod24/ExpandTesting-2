"""
generar_resumen.py
Ejecuta pytest --tb=no -q y genera un resumen ejecutivo en español
con los resultados de la suite de tests.

Uso:
    python generar_resumen.py
    python generar_resumen.py --guardar        # guarda también en resumen_ejecucion.txt
    python generar_resumen.py --archivo tests  # ejecuta solo una carpeta/archivo
"""

import subprocess
import sys
import re
import argparse
from datetime import datetime

# Forzar UTF-8 en la salida estándar para que los caracteres especiales
# se impriman correctamente en Windows (que usa cp1252 por defecto)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# Descripción legible para cada nombre de función de test
DESCRIPCIONES = {
    "test_login_exitoso":       "Login exitoso con credenciales válidas",
    "test_login_campos_vacios": "Login con ambos campos vacíos",
    "test_login_usuario_vacio": "Login con el campo usuario vacío",
    "test_login_password_vacio":"Login con el campo contraseña vacío",
    "test_usuario_erroneo":     "Login con usuario incorrecto",
    "test_password_erroneo":    "Login con contraseña incorrecta",
}


def ejecutar_pytest(objetivo: str) -> str:
    """Lanza pytest y devuelve su salida combinada (stdout + stderr)."""
    cmd = [sys.executable, "-m", "pytest", "--tb=short", "-v", "--no-header"]
    if objetivo:
        cmd.append(objetivo)

    resultado = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return resultado.stdout + resultado.stderr


def parsear_salida(salida: str) -> dict:
    """
    Extrae de la salida de pytest:
      - lista de tests con su estado (passed / failed / error)
      - conteos totales
      - duración
      - fragmentos de error por test fallido
    """
    tests = []
    conteos = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    duracion = "desconocida"

    # ── Líneas de resultado por test ─────────────────────────────────────────
    # pytest -q imprime:  test/archivo.py::nombre  PASSED/FAILED/ERROR/SKIPPED
    patron_test = re.compile(
        r"([\w/\\.\-]+::[\w\[\]-]+)\s+(PASSED|FAILED|ERROR|SKIPPED)",
        re.IGNORECASE,
    )
    for linea in salida.splitlines():
        m = patron_test.search(linea)
        if m:
            nombre_completo = m.group(1)
            estado_raw = m.group(2).lower()
            nombre_fn = nombre_completo.split("::")[-1]
            nombre_fn = re.sub(r"\[.*?\]$", "", nombre_fn)
            tests.append({
                "nombre_completo": nombre_completo,
                "nombre_fn": nombre_fn,
                "descripcion": DESCRIPCIONES.get(nombre_fn, nombre_fn.replace("_", " ")),
                "estado": estado_raw,
            })

    # ── Línea de resumen final ────────────────────────────────────────────────
    # Ejemplo: "6 passed in 38.12s"  o  "2 failed, 4 passed in 40.01s"
    patron_resumen = re.compile(
        r"(?:(\d+)\s+failed)?[,\s]*(?:(\d+)\s+passed)?[,\s]*(?:(\d+)\s+error)?[,\s]*"
        r"(?:(\d+)\s+skipped)?\s+in\s+([\d.]+)s",
        re.IGNORECASE,
    )
    m_res = patron_resumen.search(salida)
    if m_res:
        conteos["failed"]  = int(m_res.group(1) or 0)
        conteos["passed"]  = int(m_res.group(2) or 0)
        conteos["error"]   = int(m_res.group(3) or 0)
        conteos["skipped"] = int(m_res.group(4) or 0)
        duracion = f"{m_res.group(5)} segundos"

    # Si pytest -q no imprimió líneas PASSED/FAILED, reconstruir desde conteos
    if not tests and any(conteos.values()):
        # No tenemos detalle por test; al menos reflejamos los totales
        pass

    # ── Bloques de error (--tb=short) ─────────────────────────────────────────
    # Asociar cada bloque FAILED a su test para incluir el mensaje clave
    errores = {}
    bloque_actual = None
    for linea in salida.splitlines():
        if linea.startswith("FAILED "):
            bloque_actual = linea.replace("FAILED ", "").split(" - ")[0].strip()
            errores.setdefault(bloque_actual, [])
        elif linea.startswith("_ ") or linea.startswith("E "):
            if bloque_actual:
                errores[bloque_actual].append(linea.strip())
    for t in tests:
        clave = t["nombre_completo"]
        if clave in errores:
            t["error_detalle"] = " | ".join(errores[clave][:2])
        else:
            t["error_detalle"] = ""

    conteos["total"] = sum(conteos.values())
    return {"tests": tests, "conteos": conteos, "duracion": duracion}


def generar_resumen(datos: dict, salida_raw: str) -> str:
    c = datos["conteos"]
    total   = c["total"]
    pasaron = c["passed"]
    fallaron = c["failed"] + c["error"]
    omitidos = c["skipped"]
    porcentaje = round(pasaron / total * 100) if total else 0

    tests_ok   = [t for t in datos["tests"] if t["estado"] == "passed"]
    tests_mal  = [t for t in datos["tests"] if t["estado"] in ("failed", "error")]
    tests_skip = [t for t in datos["tests"] if t["estado"] == "skipped"]

    sep = "=" * 62

    lineas = [
        sep,
        "  RESUMEN EJECUTIVO DE EJECUCIÓN DE TESTS",
        sep,
        f"  Fecha:    {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"  Duración: {datos['duracion']}",
        sep,
        "",
    ]

    # ── Párrafo introductorio ─────────────────────────────────────────────────
    if total == 0:
        lineas += [
            "No se encontraron tests. Verifica que pytest esté instalado",
            "y que existan archivos test_*.py en el directorio.",
            "",
        ]
        lineas.append(sep)
        return "\n".join(lineas)

    if fallaron == 0 and omitidos == 0:
        estado_suite = "La suite completa pasó sin ningún fallo."
    elif fallaron == 0:
        estado_suite = f"La suite pasó; {omitidos} test(s) fueron omitidos."
    elif pasaron == 0:
        estado_suite = "Todos los tests fallaron. Revisión urgente necesaria."
    else:
        estado_suite = f"La suite tiene fallos que deben resolverse antes de entregar."

    lineas += [
        "RESULTADO GLOBAL",
        "-" * 40,
        (
            f"Se ejecutaron {total} tests: {pasaron} pasaron ({porcentaje} %), "
            f"{fallaron} fallaron"
            + (f", {omitidos} omitidos" if omitidos else "")
            + "."
        ),
        estado_suite,
        "",
    ]

    # ── Tests que pasaron ─────────────────────────────────────────────────────
    if tests_ok:
        lineas += ["TESTS QUE PASARON", "-" * 40]
        for t in tests_ok:
            lineas.append(f"  [OK]  {t['descripcion']}")
        lineas.append("")

    # ── Tests que fallaron ────────────────────────────────────────────────────
    if tests_mal:
        lineas += ["TESTS QUE FALLARON", "-" * 40]
        for t in tests_mal:
            lineas.append(f"  [FAIL]  {t['descripcion']}")
            if t.get("error_detalle"):
                lineas.append(f"     → {t['error_detalle'][:120]}")
        lineas.append("")

    # ── Tests omitidos ────────────────────────────────────────────────────────
    if tests_skip:
        lineas += ["TESTS OMITIDOS", "-" * 40]
        for t in tests_skip:
            lineas.append(f"  [SKIP]  {t['descripcion']}")
        lineas.append("")

    # ── Cobertura ─────────────────────────────────────────────────────────────
    lineas += [
        "QUÉ CUBRE ESTA SUITE",
        "-" * 40,
        "Tests end-to-end del formulario de login de practice.expandtesting.com:",
        "",
        "  • Acceso exitoso con credenciales válidas.",
        "  • Intento de login con usuario incorrecto.",
        "  • Intento de login con contraseña incorrecta.",
        "  • Envío del formulario con ambos campos vacíos.",
        "  • Envío del formulario solo con usuario vacío.",
        "  • Envío del formulario solo con contraseña vacía.",
        "",
        "Cada test valida: estado inicial de los campos, atributos HTML",
        "y el mensaje de error mostrado por la aplicación.",
        "",
    ]

    # ── Conclusión ────────────────────────────────────────────────────────────
    lineas += ["CONCLUSIÓN", "-" * 40]
    if fallaron == 0:
        lineas.append(
            f"Todos los {total} tests pasaron. La funcionalidad de login\n"
            "responde correctamente en todos los escenarios validados."
        )
    else:
        plural = "test" if fallaron == 1 else "tests"
        lineas.append(
            f"{fallaron} {plural} fallaron. Revisar los casos indicados\n"
            "arriba antes de continuar con el despliegue."
        )
    lineas += ["", sep]

    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser(
        description="Ejecuta pytest y genera un resumen ejecutivo en español."
    )
    parser.add_argument(
        "--archivo",
        default="",
        metavar="RUTA",
        help="Carpeta o archivo de tests a ejecutar (por defecto: todos).",
    )
    parser.add_argument(
        "--guardar",
        action="store_true",
        help="Guarda el resumen en resumen_ejecucion.txt.",
    )
    args = parser.parse_args()

    print("Ejecutando pytest...\n")
    salida_raw = ejecutar_pytest(args.archivo)

    datos = parsear_salida(salida_raw)
    resumen = generar_resumen(datos, salida_raw)

    print(resumen)

    if args.guardar:
        from pathlib import Path
        destino = Path("resumen_ejecucion.txt")
        destino.write_text(resumen, encoding="utf-8")
        print(f"\nResumen guardado en: {destino.resolve()}")


if __name__ == "__main__":
    main()
