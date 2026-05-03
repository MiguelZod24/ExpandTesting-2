import allure
import pytest
from pages.login_page import LoginPage


@allure.feature("Allure Artifacts Test")
@allure.story("Verification of Allure Attachments")
@allure.title("Test para verificar captura de artefactos en Allure")
@allure.description("Este test falla intencionalmente para verificar que se capturen screenshots, videos y traces")
@allure.severity(allure.severity_level.NORMAL)
def test_allure_artifacts_verification(page):
    """
    Test que falla intencionalmente para verificar que los artefactos
    (screenshot, video, trace) se adjunten correctamente al reporte Allure.
    """
    login_page = LoginPage(page)
    
    @allure.step("Navegar a página de login")
    def navegar_login():
        login_page.navegar()
    
    @allure.step("Ingresar credenciales incorrectas para forzar fallo")
    def ingresar_credenciales_incorrectas():
        login_page.ingresar_usuario("usuario_incorrecto")
        login_page.ingresar_password("password_incorrecto")
    
    @allure.step("Ejecutar login y verificar fallo esperado")
    def ejecutar_login_y_fallar():
        login_page.click_login()
        # Esta assertion fallará intencionalmente para probar la captura de artefactos
        error = login_page.obtener_error()
        assert "Este mensaje nunca aparecerá" in error, "Fallo intencional para probar artefactos"
    
    # Ejecutar los pasos
    navegar_login()
    ingresar_credenciales_incorrectas()
    ejecutar_login_y_fallar()
