BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "[placeholder='Username']"  # Selector mejorado con placeholder
        self.password_input = "[placeholder='Password']"  # Selector mejorado con placeholder
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.fill(self.username_input, usuario)

    def ingresar_password(self, password):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    # ---------- Validaciones ----------
    def obtener_error(self):
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        valor = self.page.get_attribute(campo, "value")
        return valor == ""

    def atributo_name(self, campo):
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        self.page.wait_for_selector(campo, timeout=5000)
        return self.page.get_attribute(campo, "value")
