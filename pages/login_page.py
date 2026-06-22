BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: Using getByRole() instead of CSS selectors where available
        self.username_input = "role=textbox[name='username']"
        self.password_input = "role=textbox[name='password']"
        self.login_button = "role=button[name='Login']"
        self.error_message = "#flash"

    def navegar(self):
        # TestDino: Ensure base URL usage through config
        self.page.goto(BASE_URL + "/login", wait_until="load")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # TestDino: Use web-first assertions for retry mechanism
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo_selector):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion adaptation with auto-retry
        return self.page.locator(campo_selector).get_attribute("value") == ""

    def atributo_name(self, campo_selector):
        """Devuelve el valor del atributo name de un input"""
        return self.page.locator(campo_selector).get_attribute("name")

    def valor_ingresado(self, campo_selector):
        """Devuelve el valor actual del input"""
        # TestDino: Ensure inputs have correct retry for their values
        return self.page.locator(campo_selector).input_value()
