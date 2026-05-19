BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # TestDino: Siempre usar selectores robustos como get_by_role
        self.username_input = self.page.get_by_role('textbox', name='username')
        self.password_input = self.page.get_by_role('textbox', name='password')
        self.login_button = self.page.get_by_role('button', name='Log in')  # Suposición del rol y nombre del botón
        self.error_message = "#flash"  # Considerar usar también un selector basado en rol para consistencia

    def navegar(self):
        # TestDino: Base URL desde config o parámetro externo
        self.page.goto(f"{BASE_URL}/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.username_input.fill(usuario)

    def ingresar_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    # ---------- Validaciones ----------
    def obtener_error(self):
        # TestDino: Asegúrate de usar wait_for_selector para una espera explícita
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.locator(self.error_message).text_content().strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        # TestDino: Web-first assertion con auto-retry - Uso de input_value para verificar contenido
        return self.page.locator(campo).input_value().strip() == ""

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.locator(campo).get_attribute("name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        # TestDino: Web-first assertions garantizan valores actuales
        return self.page.locator(campo).input_value()