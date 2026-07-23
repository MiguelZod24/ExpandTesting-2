BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: Renovado a selectores accesibles y robustos
        self.username_input = "input#username"  # Cambiado a un ID más específico
        self.password_input = "input#password"  # Cambiado a un ID más específico
        self.login_button = "button#loginButton"  # Cambiado a un ID específico
        self.error_message = "#flash"  # Mantiene consistencia

    def navegar(self):
        # TestDino: baseURL en config - Golden Rule #5
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
        return self.page.input_value(campo)