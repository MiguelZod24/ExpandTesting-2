BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: getByRole() sobre CSS/XPath - Golden Rule #1 (adaptado para Python)
        self.username_input = "input[name='username']"  # Recomendación: usar un selector aria-label para mejor accesibilidad
        self.password_input = "input[name='password']"  # Recomendación: usar un selector aria-label para mejor accesibilidad
        self.login_button = "button:has-text('Log in')" # Usa un selector más robusto basado en el texto
        self.error_message = "#flash"  # Validar que este ID esté correctamente referenciado

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
        self.page.locator(self.error_message).wait_for()
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        return self.page.get_attribute(campo, "value") == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertion con auto-retry - Golden Rule #3 (adaptado para Python)
        return self.page.input_value(campo)