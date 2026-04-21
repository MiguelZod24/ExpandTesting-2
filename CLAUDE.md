# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué hace este proyecto

Tests end-to-end automatizados para la página de login de [practice.expandtesting.com](https://practice.expandtesting.com) usando Python y Playwright. La suite valida escenarios negativos de login (usuario inválido, contraseña inválida).

## Tecnologías

- **Python 3.13** con **pytest** como runner de tests
- **Playwright** (via `playwright` + `pytest-playwright`) para automatización de navegador — corre Chromium en modo headless
- **Allure** (`allure-pytest`) para reportes enriquecidos de tests
- **pytest-html** para reportes HTML autocontenidos (usado en CI)
- **python-dotenv** para gestión de variables de entorno

## Comandos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar navegadores de Playwright (requerido una vez)
playwright install

# Ejecutar todos los tests (verbose)
pytest -v

# Ejecutar un único archivo de tests
pytest test/test_pass_erroneo.py -v

# Ejecutar un test concreto por nombre
pytest -k "test_password_erroneo" -v

# Ejecutar con resultados Allure (luego abrir el reporte)
pytest --alluredir=allure-results
allure serve allure-results

# Ejecutar con reporte HTML (igual que en CI)
pytest -v --maxfail=1 --disable-warnings --html=report.html --self-contained-html
```

## Arquitectura

El proyecto aplica el patrón **Page Object Model (POM)**:

- `pages/login_page.py` — clase `LoginPage` que encapsula todos los selectores e interacciones de la página de login. Los tests nunca llaman a Playwright directamente; siempre pasan por esta clase.
- `test/` — archivos de test que importan `LoginPage` y la usan a través del fixture `page`.
- `conftest.py` — define el fixture `page` (abre/cierra un navegador Chromium por test) y un hook `pytest_runtest_makereport` que captura un screenshot en `screenshots/` cuando un test falla y lo adjunta al reporte HTML.

### Flujo de un test

1. El fixture `page` (conftest) lanza Chromium headless y cede un objeto `Page` de Playwright.
2. El test instancia `LoginPage(page)` y llama a `navegar()` para ir a `/login`.
3. El test interactúa con la página mediante los métodos de `LoginPage` y luego valida el texto del mensaje de error en `#flash`.

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) se ejecuta en cada push/PR a `main` y diariamente a las 07:00 UTC. El pipeline:
1. Ejecuta la suite completa con `pytest-html`.
2. Sube `report.html` y la carpeta `screenshots/` como artefactos descargables.

## Convenciones de código

- Todos los métodos de `LoginPage` y los nombres de los tests están escritos en español.
- Los selectores CSS se almacenan como atributos en `LoginPage.__init__` — nunca se escriben directamente en los tests.
- Cada test valida el estado de los campos (vacío, atributo `name` correcto, valor introducido) **antes** de verificar el mensaje de error.
- El scope del fixture `page` es `function` — contexto de navegador fresco por test, sin estado compartido entre tests.
- Las credenciales válidas del sitio de práctica son usuario `practice` / contraseña `SuperSecretPassword!`.

## Objetivo de aprendizaje

Este proyecto es un portfolio personal para demostrar habilidades de QA Automation con IA integrada. El objetivo es mostrar cómo un QA Engineer utiliza Claude Code en todo el proceso de testing: desde la generación de tests y detección de fallos hasta la producción de reportes, aplicando buenas prácticas de automatización en cada etapa.

## Reglas para generar código

- **Siempre usar Page Object Model**: cualquier nueva página o componente debe tener su propia clase en `pages/`.
- **Métodos y tests en español**: nombres de funciones, variables de dominio y comentarios deben estar en español.
- **Comentarios explicativos**: añadir comentarios que expliquen el propósito de cada bloque lógico dentro del código, especialmente en los tests.
- **Nunca hardcodear selectores fuera de `LoginPage`**: los selectores CSS/XPath solo viven en la clase Page Object correspondiente.
- **Cada test debe ser independiente**: sin dependencias de orden de ejecución ni estado compartido entre tests.

## Roadmap del proyecto

Próximos pasos planificados:

1. **Generación automática de tests con IA** — usar Claude Code para proponer y escribir nuevos casos de test a partir de la especificación de la aplicación.
2. **Análisis de fallos con IA** — integrar Claude para interpretar logs y screenshots de fallos y generar un diagnóstico en lenguaje natural.
3. **Reportes inteligentes** — producir resúmenes automáticos de la ejecución en lenguaje natural, accesibles para perfiles no técnicos.
4. **Testing de APIs con Swagger** — ampliar la suite para cubrir los endpoints REST documentados en Swagger de practice.expandtesting.com.
