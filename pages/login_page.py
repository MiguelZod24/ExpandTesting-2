BASE_URL = "https://practice.expandtesting.com"

from playwright.async_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "input[name='username']"  
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    def ingresar_usuario(self, usuario):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    def obtener_error(self):
        error_element = self.page.locator(self.error_message)
        expect(error_element).to_be_visible(timeout=5000)
        return error_element.text_content().strip()

    def campo_vacio(self, campo):
        campo_elemento = self.page.locator(campo)
        expect(campo_elemento).to_have_attribute("value", "")
        valor = campo_elemento.get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        campo_elemento = self.page.locator(campo)
        return campo_elemento.get_attribute("name")

    def valor_ingresado(self, campo):
        campo_elemento = self.page.locator(campo)
        return campo_elemento.input_value()