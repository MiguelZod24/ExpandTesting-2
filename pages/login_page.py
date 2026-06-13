BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores corregidos de acuerdo con la "Golden Rule #1": primero get_by_role antes que CSS/XPath
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = self.page.locator("#flash")

    def navegar(self):
        # Golden Rule #5: usar rutas relativas con baseURL proporcionada en la configuración
        self.page.goto("/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Golden Rule #3: Web-first assertions con auto-retry
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # Golden Rule #3: Web-first assertion con auto-retry
        valor = campo.get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # Golden Rule #3: Web-first assertion con auto-retry
        return campo.input_value()