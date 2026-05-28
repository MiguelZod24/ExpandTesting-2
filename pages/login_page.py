BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Ajuste de selectores según la regla #1
        self.username_input = 'input#username'  
        self.password_input = 'input#password' 
        self.login_button = 'button[type="submit"]'
        self.error_message = '#flash'

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
        valor = self.page.get_attribute(campo, "value") or ""
        return valor.strip() == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertions con auto-retry - Golden Rule #3 (adaptado para Python)
        return self.page.input_value(campo)
