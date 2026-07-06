BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Mejora los selectores con get_by_role como requerido por Golden Rule #1
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = "#flash"  # Usamos un selector único para mensajes de error

    def navegar(self):
        self.page.goto("/login")

    def ingresar_usuario(self, usuario):
        # Usa interacción de Playwright específica para campos de entrada
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        # Usa interacción de Playwright específica para campos de entrada
        self.password_input.fill(password)

    def click_login(self):
        # Usa la interacción en el botón identificado por get_by_role
        self.login_button.click()

    def obtener_error(self):
        # Valida la existencia del mensaje de error con auto-reintentos
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío, dado su referencia."""
        return campo.input_value().strip() == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un elemento campo de entrada."""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual ingresado en el campo."""
        return campo.input_value()