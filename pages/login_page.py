BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "[name='username']"  # Reemplazado por selector más adecuado
        self.password_input = "[name='password']"  # Reemplazado por selector más adecuado
        self.login_button = "button:has-text('Login')"  # Uso más robusto de has-text para buscar el botón por texto
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        self.page.locator(self.error_message).wait_for(state="visible", timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo):
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        return self.page.locator(campo).input_value()