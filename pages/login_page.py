BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores corregidos utilizando get_by_role para una mayor confiabilidad
        self.username_input = self.page.get_by_role("textbox", {"name": "username"})
        self.password_input = self.page.get_by_role("textbox", {"name": "password"})
        self.login_button = self.page.get_by_role("button", {"name": "Login"})
        self.error_message = self.page.locator("#flash")

    def navegar(self):
        # Usar baseURL desde la configuración para un enfoque más flexible en las pruebas
        self.page.goto("/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Espera que aparezca el mensaje de error antes de recuperar el texto
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        return campo.get_attribute("value") == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        return campo.input_value()