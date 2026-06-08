BASE_URL = "https://practice.expandtesting.com"

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Selectores actualizados para cumplir con Golden Rule #1
        self.username_input = "input#username"  # Usando ID para un selector más robusto
        self.password_input = "input#password"  # Usando ID para un selector más robusto
        self.login_button = "button[type='submit']"
        self.error_message = "#flash"

    def navegar(self):
        # Navegar a una URL completa con prefijo BASE_URL
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
        # Validación con espera hasta 5s por la aparición del mensaje de error
        self.page.wait_for_selector(self.error_message, timeout=5000)
        return self.page.text_content(self.error_message).strip()

    def campo_vacio(self, campo):
        """Devuelve True si el campo está vacío"""
        valor = self.page.get_attribute(campo, "value")
        return not valor  # Cambiado para verificar si no hay valor

    def atributo_name(self, campo):
        """Devuelve el valor del atributo name de un input"""
        return self.page.get_attribute(campo, "name")

    def valor_ingresado(self, campo):
        """Devuelve el valor actual del input"""
        return self.page.input_value(campo)