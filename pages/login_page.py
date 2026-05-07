BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Actualización de selectores para seguir mejores prácticas (usando get_by_role, aria-label o nombre descriptivo)
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Log in")
        self.error_message = self.page.locator("#flash")

    def navegar(self):
        # Usar la constante BASE_URL para navegar
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Verificación con reintento automático mediante espera explícita
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        return campo.input_value() == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # Utiliza directamente el método input_value
        return campo.input_value()