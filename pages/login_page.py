BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Modificados los selectores para cumplir con Golden Rule #1
        self.username_input = "input#username"  # Cambiado para ser más específico
        self.password_input = "input#password"  # Cambiado para ser más específico
        self.login_button = "button#login"  # Asegurar que es único
        self.error_message = "#flash"  # Mantenido porque cumple con reglas

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
        """Devuelve el valor actual del input"""
        return self.page.locator(campo).input_value()