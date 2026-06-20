BASE_URL = "https://practice.expandtesting.com"

from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = self.page.locator("input[name='username']")
        self.password_input = self.page.locator("input[name='password']")
        self.login_button = self.page.locator("button[type='submit']")
        self.error_message = self.page.locator("#flash")

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario: str):
        self.username_input.fill(usuario)

    def ingresar_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self) -> str:
        self.error_message.wait_for()
        return self.error_message.text_content().strip()

    def campo_vacio(self, campo_locator):
        """Devuelve True si el campo está vacío"""
        return campo_locator.get_attribute("value") == ""

    def atributo_name(self, campo_locator):
        """Devuelve el valor del atributo name de un input"""
        return campo_locator.get_attribute("name")

    def valor_ingresado(self, campo_locator) -> str:
        """Devuelve el valor actual del input"""
        return campo_locator.input_value()