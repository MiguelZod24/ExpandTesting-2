BASE_URL = "https://practice.expandtesting.com"

from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = self.page.get_by_role("textbox", name="username")
        self.password_input = self.page.get_by_role("textbox", name="password")
        self.login_button = self.page.get_by_role("button", name="Log In")
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    def ingresar_usuario(self, usuario: str):
        self.username_input.fill(usuario)

    def ingresar_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def obtener_error(self) -> str:
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        valor = campo.input_value()
        return valor == ""

    def atributo_name(self, campo):
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        return campo.input_value()