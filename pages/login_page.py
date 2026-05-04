BASE_URL = 'https://practice.expandtesting.com'

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: getByRole() sobre CSS/XPath - Golden Rule #1 (adaptado para Python)
        self.username_input = "[name='username']"  # Ajustado a selector más eficiente
        self.password_input = "[name='password']"  # Ajustado a selector más eficiente
        self.login_button = "[role='button'][type='submit']"  # Mejor uso del rol sobre type
        self.error_message = '#flash'

    def navegar(self):
        # TestDino: baseURL en config - Golden Rule #5
        self.page.goto(f"{BASE_URL}/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.fill(self.username_input, usuario)

    def ingresar_password(self, password):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    # ---------- Validaciones ----------
    def obtener_error(self):
        # TestDino: Web-first assertions con auto-retry - Golden Rule #3 (adaptado para Python)
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        valor = self.page.get_attribute(campo, "value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        self.page.wait_for_selector(campo, timeout=5000)
        return self.page.input_value(campo)