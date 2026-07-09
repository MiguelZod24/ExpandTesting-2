BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores refactorizados siguiendo la regla de getByRole en lugar de selectores específicos
        self.username_input = "role=textbox[name=Username]"
        self.password_input = "role=textbox[name=Password]"
        self.login_button = "role=button[name=Login]"
        self.error_message = "role=alert"

    def navegar(self):
        self.page.goto("/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.get_by_role("textbox", name="Username").fill(usuario)

    def ingresar_password(self, password):
        self.page.get_by_role("textbox", name="Password").fill(password)

    def click_login(self):
        self.page.get_by_role("button", name="Login").click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        self.page.get_by_role("alert").wait_for(timeout=5000)
        return self.page.get_by_role("alert").text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        valor = self.page.get_by_role("textbox", name=campo).evaluate("element => element.value")
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_by_role("textbox", name=campo).get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        return self.page.get_by_role("textbox", name=campo).input_value()