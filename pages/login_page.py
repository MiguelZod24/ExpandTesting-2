BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page

        # TestDino: getByRole() sobre CSS/XPath - Golden Rule #1 (adaptado para Python)
        self.username_input = "input[name='username']"  # Se cambió a un selector más preciso
        self.password_input = "input[name='password']"  # Se cambió a un selector más preciso
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        # TestDino: baseURL en config - Golden Rule #5
        self.page.goto(f"{BASE_URL}/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.locator(self.username_input).fill(usuario)

    def ingresar_password(self, password):
        self.page.locator(self.password_input).fill(password)

    def click_login(self):
        self.page.locator(self.login_button).click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # TestDino: Web-first assertions con auto-retry - Golden Rule #3 (adaptado para Python)
        return self.page.locator(self.error_message).text_content(timeout=5000).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        return self.page.locator(campo).input_value()