BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "input[name='username']" 
        self.password_input = "input[name='password']" 
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(f"{BASE_URL}/login")

    def ingresar_usuario(self, usuario):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    def obtener_error(self):
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo):
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        return self.page.locator(campo).input_value()