BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Corrección: Usar selectores con get_by_role según la regla Golden Rule #1
        self.username_input = self.page.get_by_role("textbox", name="username")
        self.password_input = self.page.get_by_role("textbox", name="password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = "#flash"

    def navegar(self):
        # Navegar directamente a la URL a través del uso del base URL
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Esperar al selector y devolver el texto
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        valor = campo.get_attribute("value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return campo.get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        return campo.input_value()