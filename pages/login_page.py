BASE_URL = 'https://practice.expandtesting.com'

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Ajuste en selectores utilizando get_by_role para mejor precisión
        self.username_input = '[name="username"]'  # Selector ajustado
        self.password_input = '[name="password"]'  # Selector ajustado
        self.login_button = 'role=button[name="Log In"]'  # Cambiado a get_by_role con nombre descriptivo
        self.error_message = '#flash'

    def navegar(self):
        self.page.goto(f"{BASE_URL}/login")  # Corrige la falta de baseURL según la Golden Rule #5

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
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        return self.page.locator(campo).input_value()