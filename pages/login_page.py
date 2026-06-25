BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores ajustados para usar get_by_role
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.login_button = "button:has-text('Login')"
        self.error_message = "#flash"

    def navegar(self):
        # Navega a la URL base del login
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
        # Validación con espera automática
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        valor = self.page.locator(campo).get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input con espera automática"""
        return self.page.locator(campo).input_value()