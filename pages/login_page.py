BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Ajuste de selectores utilizando get_by_role (Golden Rule #1)
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        # Navegación utilizando baseURL (Golden Rule #5)
        self.page.goto(f"{BASE_URL}/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.fill(self.username_input, usuario)

    def ingresar_password(self, password):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Validación con auto-retry para extraer el mensaje de error (Golden Rule #3)
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        # Revisión si el campo está vacío
        self.page.wait_for_selector(campo, timeout=5000)
        valor = self.page.evaluate(f'(element) => element.value', self.page.query_selector(campo))
        return valor == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        self.page.wait_for_selector(campo, timeout=5000)
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        self.page.wait_for_selector(campo, timeout=5000)
        return self.page.input_value(campo)
