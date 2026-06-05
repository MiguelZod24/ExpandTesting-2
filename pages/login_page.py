BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores mejorados basados en roles para cumplir con las mejores prácticas de testeo
        self.username_input = "[placeholder='Username']"  # Suponiendo que el input tiene un placeholder claro
        self.password_input = "[placeholder='Password']"  # Suponiendo que el input tiene un placeholder claro
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        # Navegar hacía la URL base del login
        self.page.goto(BASE_URL + "/login")

    # ---------- Interacción ----------
    def ingresar_usuario(self, usuario):
        self.page.fill(self.username_input, usuario)

    def ingresar_password(self, password):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    # ---------- Validaciones ----------
    def obtener_error(self):
        # Implementar espera activa y obtener el contenido de texto del mensaje de error
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        valor = self.page.get_attribute(campo, "value")
        return not valor  # Verifica si no hay valor

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        self.page.wait_for_selector(campo, timeout=5000)  # Agregar espera activa para garantizar visibilidad
        return self.page.input_value(campo)
