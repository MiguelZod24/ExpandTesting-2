import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

# Fixture de Playwright para abrir/cerrar navegador
@pytest.fixture(scope="function")
def page():
    """Fixture que abre el navegador antes de cada test y lo cierra al final."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


# Hook para adjuntar screenshots al reporte HTML y guardarlos en carpeta
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page_fixture = item.funcargs.get("page", None)
        if page_fixture:
            # Carpeta para screenshots
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Nombre único: test + fecha/hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}_{timestamp}.png")

            page_fixture.screenshot(path=screenshot_path)

            # Adjuntar al reporte HTML
            if "pytest_html" in item.config.pluginmanager.list_name_plugin():
                extra = getattr(result, "extra", [])
                extra.append(pytest_html.extras.png(screenshot_path))
                result.extra = extra


# Hook para inicializar pytest-html
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")




