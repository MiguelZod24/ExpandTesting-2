BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores actualizados usando roles y accesibilidad para mayor robustez
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        """Navegar a la página de login."""
        # Este método utiliza relativa a BASE_URL de Playwright config.
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        """Ingresa el nombre de usuario en el campo correspondiente."""
        self.page.fill(self.username_input, usuario)

    def ingresar_password(self, password):
        """Ingresa la contraseña en el campo correspondiente."""
        self.page.fill(self.password_input, password)

    def click_login(self):
        """Simula un clic en el botón de iniciar sesión."""
        self.page.click(self.login_button)

    # ---------- Validaciones ----------
    def obtener_error(self):
        """Obtiene el mensaje de error después de un intento fallido de login."""
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío."""
        valor = self.page.get_attribute(campo, "value")
        return not valor  # Simplificado para verificar si está vacío

    def atributo_name(self, campo):
        """Obtiene el valor del atributo `name` de un input."""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Obtiene el valor actual de un input."""
        return self.page.input_value(campo)