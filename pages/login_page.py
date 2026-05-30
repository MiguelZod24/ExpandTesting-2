BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Mejorando los selectores según la regla "getByRole sobre CSS/XPath"
        self.username_input = self.page.get_by_role("textbox", name="username")
        self.password_input = self.page.get_by_role("textbox", name="password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = "#flash"

    def navegar(self):
        self.page.goto(f"{BASE_URL}/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        valor = campo.get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        return campo.input_value()