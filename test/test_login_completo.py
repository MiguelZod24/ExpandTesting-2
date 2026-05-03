from pages.login_page import LoginPage
import allure


# ─────────────────────────────────────────────
# CASO 1: Login exitoso con credenciales válidas
# ─────────────────────────────────────────────
@allure.feature("Autenticación")
@allure.story("Login Exitoso")
@allure.title("Login exitoso con credenciales válidas")
@allure.description("Verifica que un usuario puede iniciar sesión correctamente con credenciales válidas")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "regression")
def test_login_exitoso(page):
    @allure.step("Navegar a página de login")
    def navegar_login(login_page):
        login_page.navegar()

    @allure.step("Validar campos vacíos iniciales")
    def validar_campos_vacios(login_page):
        assert login_page.campo_vacio(login_page.username_input)
        assert login_page.campo_vacio(login_page.password_input)

    @allure.step("Validar atributos name de los campos")
    def validar_atributos_name(login_page):
        assert login_page.atributo_name(login_page.username_input) == "username"
        assert login_page.atributo_name(login_page.password_input) == "password"

    @allure.step("Ingresar credenciales válidas")
    def ingresar_credenciales_validas(login_page):
        login_page.ingresar_usuario("practice")
        login_page.ingresar_password("SuperSecretPassword!")

    @allure.step("Validar datos ingresados")
    def validar_datos_ingresados(login_page):
        assert login_page.valor_ingresado(login_page.username_input) == "practice"
        assert login_page.valor_ingresado(login_page.password_input) == "SuperSecretPassword!"

    @allure.step("Ejecutar login y verificar éxito")
    def ejecutar_login_exitoso(login_page):
        login_page.click_login()
        mensaje = login_page.obtener_error()
        assert "You logged into a secure area!" in mensaje

    login_page = LoginPage(page)

    # Navegar a la página de login
    navegar_login(login_page)

    # Validar que los campos vienen vacíos al cargar la página
    validar_campos_vacios(login_page)

    # Validar que los campos tienen el atributo name correcto
    validar_atributos_name(login_page)

    # Ingresar credenciales válidas del entorno de práctica
    ingresar_credenciales_validas(login_page)

    # Validar que los datos fueron ingresados correctamente antes de enviar
    validar_datos_ingresados(login_page)

    # Click en el botón de login y verificar el mensaje de éxito en el flash
    ejecutar_login_exitoso(login_page)


# ──────────────────────────────────────────────────────
# CASO 2: Ambos campos vacíos — sin ingresar ningún dato
# ──────────────────────────────────────────────────────
@allure.feature("Autenticación")
@allure.story("Validación de Campos")
@allure.title("Login con ambos campos vacíos")
@allure.description("Verifica el comportamiento cuando ambos campos de login están vacíos")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("validation", "negative")
def test_login_campos_vacios(page):
    login_page = LoginPage(page)

    # Navegar a la página de login
    login_page.navegar()

    # Validar que los campos vienen vacíos al cargar la página
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar que los campos tienen el atributo name correcto
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # No se ingresa ningún dato — se envía el formulario completamente vacío
    # El sitio valida el username primero, por lo que el error esperado es sobre el usuario
    login_page.click_login()
    error = login_page.obtener_error()
    assert "Your username is invalid!" in error


# ─────────────────────────────────────────────────────────────────
# CASO 3: Solo el campo usuario vacío (la contraseña sí está rellena)
# ─────────────────────────────────────────────────────────────────
@allure.feature("Autenticación")
@allure.story("Validación de Campos")
@allure.title("Login con usuario vacío y contraseña válida")
@allure.description("Verifica el comportamiento cuando el campo usuario está vacío pero la contraseña tiene valor")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("validation", "negative")
def test_login_usuario_vacio(page):
    login_page = LoginPage(page)

    # Navegar a la página de login
    login_page.navegar()

    # Validar que los campos vienen vacíos al cargar la página
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar que los campos tienen el atributo name correcto
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # Solo se rellena la contraseña; el usuario se deja vacío a propósito
    login_page.ingresar_password("SuperSecretPassword!")

    # Confirmar que el campo usuario sigue vacío y la contraseña tiene valor
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.valor_ingresado(login_page.password_input) == "SuperSecretPassword!"

    # Click en login y verificar que el error apunta al campo usuario
    login_page.click_login()
    error = login_page.obtener_error()
    assert "Your username is invalid!" in error


# ─────────────────────────────────────────────────────────────────
# CASO 4: Solo el campo contraseña vacío (el usuario sí está relleno)
# ─────────────────────────────────────────────────────────────────
@allure.feature("Autenticación")
@allure.story("Validación de Campos")
@allure.title("Login con contraseña vacía y usuario válido")
@allure.description("Verifica el comportamiento cuando el campo contraseña está vacío pero el usuario tiene valor")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("validation", "negative")
def test_login_clave_vacia(page):
    login_page = LoginPage(page)

    # Navegar a la página de login
    login_page.navegar()

    # Validar que los campos vienen vacíos al cargar la página
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar que los campos tienen el atributo name correcto
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # Solo se rellena el usuario; la contraseña se deja vacía a propósito
    login_page.ingresar_usuario("practice")

    # Confirmar que el usuario tiene valor y el campo contraseña sigue vacío
    assert login_page.valor_ingresado(login_page.username_input) == "practice"
    assert login_page.campo_vacio(login_page.password_input)

    # Click en login y verificar que el error apunta al campo contraseña
    login_page.click_login()
    error = login_page.obtener_error()
    assert "Your password is invalid!" in error
