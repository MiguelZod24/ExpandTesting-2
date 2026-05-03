import pytest
import allure
from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import glob

# TestDino: baseURL en config - Golden Rule #5
BASE_URL = os.getenv("BASE_URL", "https://practice.expandtesting.com")

# Fixture de Playwright para abrir/cerrar navegador
@pytest.fixture(scope="function")
def page():
    """Fixture que abre el navegador antes de cada test y lo cierra al final."""
    with sync_playwright() as p:
        # Crear directorios para artefactos
        artifacts_dir = "test_artifacts"
        videos_dir = os.path.join(artifacts_dir, "videos")
        traces_dir = os.path.join(artifacts_dir, "traces")
        screenshots_dir = os.path.join(artifacts_dir, "screenshots")
        
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(traces_dir, exist_ok=True)
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Configurar browser con video y trace
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-web-security"]
        )
        
        # TestDino: baseURL en config - Golden Rule #5
        context = browser.new_context(
            base_url=BASE_URL,
            record_video_dir=videos_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        
        # Iniciar trace logging
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )
        
        page = context.new_page()
        yield page
        
        # Detener trace al final del fixture (solo si no se detuvo en el hook)
        try:
            final_trace_path = os.path.join(traces_dir, f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
            context.tracing.stop(path=final_trace_path)
        except Exception:
            pass  # El trace ya fue detenido en el hook si el test falló
        
        context.close()
        browser.close()


# Hook para adjuntar screenshots, videos y traces al reporte Allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page_fixture = item.funcargs.get("page", None)
        if page_fixture:
            # Directorios de artefactos
            artifacts_dir = "test_artifacts"
            screenshots_dir = os.path.join(artifacts_dir, "screenshots")
            videos_dir = os.path.join(artifacts_dir, "videos")
            traces_dir = os.path.join(artifacts_dir, "traces")
            
            os.makedirs(screenshots_dir, exist_ok=True)
            os.makedirs(videos_dir, exist_ok=True)
            os.makedirs(traces_dir, exist_ok=True)
            
            # Generar timestamp único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name_base = f"{item.name}_{timestamp}"
            
            # Capturar screenshot
            screenshot_path = os.path.join(screenshots_dir, f"{test_name_base}.png")
            page_fixture.screenshot(path=screenshot_path)
            
            # Adjuntar screenshot a Allure
            allure.attach.file(
                screenshot_path, 
                name=f"Screenshot - {item.name}", 
                attachment_type=allure.attachment_type.PNG
            )
            
            # Guardar el contexto para obtener el video y trace específicos
            context = page_fixture.context
            
            # NO cerrar la página aquí - el video se guarda al cerrar el contexto
            # page_fixture.close()  # Comentado para evitar problemas con video
            
            # Esperar un momento para que se guarde el video
            import time
            time.sleep(1)
            
            # Buscar video del test actual (el más reciente)
            video_files = glob.glob(os.path.join(videos_dir, "*.webm"))
            if video_files:
                # Obtener el video más reciente (de este test)
                latest_video = max(video_files, key=os.path.getctime)
                
                # Verificar que el video no esté vacío
                if os.path.getsize(latest_video) > 0:
                    # Copiar con nombre específico para evitar conflictos
                    specific_video_path = os.path.join(videos_dir, f"{test_name_base}.webm")
                    try:
                        import shutil
                        shutil.copy2(latest_video, specific_video_path)
                        
                        # Adjuntar video a Allure
                        allure.attach.file(
                            specific_video_path,
                            name=f"Video - {item.name}",
                            attachment_type=allure.attachment_type.WEBM
                        )
                    except Exception as e:
                        print(f"Error al copiar video: {e}")
                else:
                    print(f"Video vacío encontrado: {latest_video}")
            
            # Generar trace específico para este test
            trace_path = os.path.join(traces_dir, f"{test_name_base}.zip")
            try:
                context.tracing.stop(path=trace_path)
                
                # Adjuntar trace a Allure
                allure.attach.file(
                    trace_path,
                    name=f"Trace - {item.name}",
                    attachment_type=allure.attachment_type.ZIP
                )
                
                # Reiniciar tracing para siguientes tests
                context.tracing.start(
                    screenshots=True,
                    snapshots=True,
                    sources=True
                )
            except Exception as e:
                print(f"Error al guardar trace: {e}")

            # Adjuntar al reporte HTML (si está disponible)
            if "pytest_html" in item.config.pluginmanager.list_name_plugin():
                extra = getattr(result, "extra", [])
                extra.append(pytest_html.extras.png(screenshot_path))
                result.extra = extra


# Hook para inicializar pytest-html
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")
