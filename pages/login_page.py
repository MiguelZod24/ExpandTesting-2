BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: get_by_role() sobre CSS/XPath - Golden Rule #1 (adaptado para Python)
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = "#flash"

    def navegar(self):
        # TestDino: baseURL en config - Golden Rule #5
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
        # TestDino: Web-first assertions con auto-retry - Golden Rule #3 (adaptado para Python)
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        valor = campo.evaluate("element => element.value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        return campo.input_value()