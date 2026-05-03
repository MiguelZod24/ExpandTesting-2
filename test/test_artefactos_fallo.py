from pages.login_page import LoginPage
import allure

@allure.feature("Autenticación")
@allure.story("Pruebas de Fallo")
@allure.title("Test deliberado para probar captura de artefactos")
@allure.description("Este test falla intencionalmente para verificar que se capturen screenshots, videos y traces")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("debug", "artifacts")
def test_fallo_intencional(page):
    login_page = LoginPage(page)
    
    # Navegar a la página de login
    login_page.navegar()
    
    # Ingresar credenciales válidas
    login_page.ingresar_usuario("practice")
    login_page.ingresar_password("SuperSecretPassword!")
    
    # Click en login
    login_page.click_login()
    
    # Este assertion fallará intencionalmente para probar captura de artefactos
    mensaje = login_page.obtener_error()
    assert "Este mensaje nunca aparecerá" in mensaje
