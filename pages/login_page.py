BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: Mejorando selectores para mayor confiabilidad utilizando getByRole
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error_message = "#flash"

    def navegar(self):
        # TestDino: Acceso directo usando el BASE_URL
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
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo_selector):
        # Verifica si un campo está vacío basado en su selector
        campo = self.page.query_selector(campo_selector)
        if campo:
            valor = campo.get_attribute("value")
            return valor == ""
        return False

    def atributo_name(self, campo_selector):
        campo = self.page.query_selector(campo_selector)
        if campo:
            return campo.get_attribute("name")
        return None

    def valor_ingresado(self, campo_selector):
        campo = self.page.query_selector(campo_selector)
        if campo:
            return campo.input_value()
        return ""