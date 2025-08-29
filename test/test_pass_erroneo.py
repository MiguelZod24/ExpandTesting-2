from pages.login_page import LoginPage

def test_password_erroneo(page):
    login_page = LoginPage(page)

    login_page.navegar()

    # Validar que los campos vienen vacíos
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar atributos name
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # Ingresar datos
    login_page.ingresar_usuario("practice")
    login_page.ingresar_password("PasswordInvalido123")

    # Validar que los datos fueron ingresados
    assert login_page.valor_ingresado(login_page.username_input) == "practice"
    assert login_page.valor_ingresado(login_page.password_input) == "PasswordInvalido123"

    # Click login y validar error
    login_page.click_login()
    error = login_page.obtener_error()
    assert "Your password is invalid!" in error




