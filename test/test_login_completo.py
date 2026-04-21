from pages.login_page import LoginPage


# ─────────────────────────────────────────────
# CASO 1: Login exitoso con credenciales válidas
# ─────────────────────────────────────────────
def test_login_exitoso(page):
    login_page = LoginPage(page)

    # Navegar a la página de login
    login_page.navegar()

    # Validar que los campos vienen vacíos al cargar la página
    assert login_page.campo_vacio(login_page.username_input)
    assert login_page.campo_vacio(login_page.password_input)

    # Validar que los campos tienen el atributo name correcto
    assert login_page.atributo_name(login_page.username_input) == "username"
    assert login_page.atributo_name(login_page.password_input) == "password"

    # Ingresar credenciales válidas del entorno de práctica
    login_page.ingresar_usuario("practice")
    login_page.ingresar_password("SuperSecretPassword!")

    # Validar que los datos fueron ingresados correctamente antes de enviar
    assert login_page.valor_ingresado(login_page.username_input) == "practice"
    assert login_page.valor_ingresado(login_page.password_input) == "SuperSecretPassword!"

    # Click en el botón de login y verificar el mensaje de éxito en el flash
    login_page.click_login()
    mensaje = login_page.obtener_error()
    assert "You logged into a secure area!" in mensaje


# ──────────────────────────────────────────────────────
# CASO 2: Ambos campos vacíos — sin ingresar ningún dato
# ──────────────────────────────────────────────────────
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
def test_login_password_vacio(page):
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
