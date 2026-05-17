BASE_URL = "https://practice.expandtesting.com"

from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "[name='username']"
        self.password_input = "[name='password']"
        self.login_button = "[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario: str):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password: str):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    # ---------- Validaciones ----------
    def obtener_error(self) -> str:
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo: str) -> bool:
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo: str) -> str:
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo: str) -> str:
        return self.page.locator(campo).input_value()