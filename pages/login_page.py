BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: Mejorar los selectores a get_by_role
        self.username_input = "input[name='username']"  # Cambiar si hay un mejor selector accesible
        self.password_input = "input[name='password']"  # Cambiar si hay un mejor selector accesible
        self.login_button = "[role='button'][name='Login']"  # Usar rol y nombre accesible, si es posible
        self.error_message = "#flash"  # Error actual visible si las credenciales fallan

    def navegar(self):
        # TestDino: baseURL en config - Golden Rule #5
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
        # TestDino: Web-first assertions con auto-retry - Golden Rule #3 (adaptado para Python)
        self.page.wait_for_selector(self.error_message, state="visible", timeout=5000)
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
