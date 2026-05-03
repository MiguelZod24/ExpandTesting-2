from pages.login_page import LoginPage
import allure

@allure.feature("Autenticación")
@allure.story("Credenciales Inválidas")
@allure.title("Login con usuario incorrecto")
@allure.description("Verifica el comportamiento cuando se ingresa un usuario incorrecto con contraseña válida")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("security", "negative")
def test_usuario_erroneo(page):
    login_page = LoginPage(page)

    # Navegar a login
    login_page.navegar()

    # Validar que los campos vienen vacíos
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar que los campos tienen el atributo name correcto
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # Ingresar datos
    login_page.ingresar_usuario("usuario_invalido")
    login_page.ingresar_password("SuperSecretPassword!")

    # Validar que los datos fueron ingresados correctamente
    assert login_page.valor_ingresado(login_page.username_input) == "usuario_invalido"
    assert login_page.valor_ingresado(login_page.password_input) == "SuperSecretPassword!"

    # Click login y validar error
    login_page.click_login()
    error = login_page.obtener_error()
    assert "Your username is invalid!" in error


