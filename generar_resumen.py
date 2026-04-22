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
    "test_login_clave_vacia":   "Login con el campo contraseña vacío",
    "test_usuario_erroneo":     "Login con usuario incorrecto",
    "test_clave_erronea":       "Login con contraseña incorrecta",
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


def _parsear_tests(salida: str) -> list:
    """Extrae la lista de tests con su estado desde la salida de pytest."""
    ESTADOS = {"PASSED", "FAILED", "ERROR", "SKIPPED"}
    tests = []
    for linea in salida.splitlines():
        partes = linea.split()
        if len(partes) < 2:
            continue
        if partes[1].upper() not in ESTADOS:
            continue
        if "::" not in partes[0]:
            continue
        nombre_completo = partes[0]
        estado_raw = partes[1].lower()
        nombre_fn = nombre_completo.split("::")[-1]
        if nombre_fn.endswith("]") and "[" in nombre_fn:
            nombre_fn = nombre_fn[:nombre_fn.rindex("[")]
        tests.append({
            "nombre_completo": nombre_completo,
            "nombre_fn": nombre_fn,
            "descripcion": DESCRIPCIONES.get(nombre_fn, nombre_fn.replace("_", " ")),
            "estado": estado_raw,
        })
    return tests


def _parsear_conteos(salida: str) -> tuple:
    """Extrae conteos totales y duración desde la línea de resumen de pytest."""
    conteos = {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    duracion = "desconocida"

    for linea in salida.splitlines():
        if " in " not in linea:
            continue
        tokens = linea.strip("= ").replace(",", "").split()
        if not tokens or not tokens[-1].endswith("s"):
            continue
        try:
            float(tokens[-1][:-1])
        except ValueError:
            continue
        if not any(kw in linea.lower() for kw in ("passed", "failed", "error", "skipped")):
            continue
        i = 0
        while i < len(tokens) - 1:
            if tokens[i].isdigit() and tokens[i + 1].lower() in conteos:
                conteos[tokens[i + 1].lower()] = int(tokens[i])
            i += 1
        duracion = f"{tokens[-1][:-1]} segundos"
        break

    return conteos, duracion


def _parsear_errores(salida: str, tests: list) -> None:
    """Asocia fragmentos de error a cada test fallido (modifica tests in-place)."""
    errores = {}
    bloque_actual = None
    for linea in salida.splitlines():
        if linea.startswith("FAILED "):
            bloque_actual = linea.replace("FAILED ", "").split(" - ")[0].strip()
            errores.setdefault(bloque_actual, [])
        elif (linea.startswith("_ ") or linea.startswith("E ")) and bloque_actual:
            errores[bloque_actual].append(linea.strip())

    for t in tests:
        clave = t["nombre_completo"]
        t["error_detalle"] = " | ".join(errores[clave][:2]) if clave in errores else ""


def parsear_salida(salida: str) -> dict:
    """
    Extrae de la salida de pytest:
      - lista de tests con su estado (passed / failed / error)
      - conteos totales
      - duración
      - fragmentos de error por test fallido
    """
    tests = _parsear_tests(salida)
    conteos, duracion = _parsear_conteos(salida)
    _parsear_errores(salida, tests)

    conteos["total"] = sum(conteos.values())
    return {"tests": tests, "conteos": conteos, "duracion": duracion}


def _seccion_tests_ok(tests_ok: list) -> list:
    """Devuelve las líneas del bloque 'tests que pasaron'."""
    if not tests_ok:
        return []
    lineas = ["TESTS QUE PASARON", "-" * 40]
    for t in tests_ok:
        lineas.append(f"  [OK]  {t['descripcion']}")
    lineas.append("")
    return lineas


def _seccion_tests_mal(tests_mal: list) -> list:
    """Devuelve las líneas del bloque 'tests que fallaron'."""
    if not tests_mal:
        return []
    lineas = ["TESTS QUE FALLARON", "-" * 40]
    for t in tests_mal:
        lineas.append(f"  [FAIL]  {t['descripcion']}")
        if t.get("error_detalle"):
            lineas.append(f"     → {t['error_detalle'][:120]}")
    lineas.append("")
    return lineas


def _seccion_tests_skip(tests_skip: list) -> list:
    """Devuelve las líneas del bloque 'tests omitidos'."""
    if not tests_skip:
        return []
    lineas = ["TESTS OMITIDOS", "-" * 40]
    for t in tests_skip:
        lineas.append(f"  [SKIP]  {t['descripcion']}")
    lineas.append("")
    return lineas


def _seccion_conclusion(fallaron: int, total: int) -> list:
    """Devuelve las líneas del bloque 'conclusión'."""
    lineas = ["CONCLUSIÓN", "-" * 40]
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
    return lineas


def generar_resumen(datos: dict) -> str:
    c = datos["conteos"]
    total    = c["total"]
    pasaron  = c["passed"]
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
        estado_suite = "La suite tiene fallos que deben resolverse antes de entregar."

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

    lineas += _seccion_tests_ok(tests_ok)
    lineas += _seccion_tests_mal(tests_mal)
    lineas += _seccion_tests_skip(tests_skip)

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

    lineas += _seccion_conclusion(fallaron, total)
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
    resumen = generar_resumen(datos)

    print(resumen)

    if args.guardar:
        from pathlib import Path
        destino = Path("resumen_ejecucion.txt")
        destino.write_text(resumen, encoding="utf-8")
        print(f"\nResumen guardado en: {destino.resolve()}")


if __name__ == "__main__":
    main()
