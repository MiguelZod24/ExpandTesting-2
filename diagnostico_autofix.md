Diagnóstico: 1. La navegación a la URL de inicio de sesión no estaba utilizando el prefijo de BASE_URL como se especifica en las reglas. Esto se corrigió concatenando BASE_URL con '/login' en el método navegar().
2. Los selectores previamente usados para username_input y password_input eran genéricos y basados en atributos 'name'. Se corrigieron para utilizar selectores más específicos y evitar posibles colisiones (recomendación por TestDino Golden Rules).
3. Se cambió 'self.page.text_content()' por 'self.page.inner_text()' en el método obtener_error() para asegurar la captura precisa del texto visible sin espacios innecesarios.
4. Se agregó 'self.page.wait_for_selector(campo, timeout=5000)' en métodos que interactúan con un campo específico, como campo_vacio() y valor_ingresado(), para evitar errores por falta de sincronización al intentar interactuar con el DOM antes de que este esté listo.
Archivo: pages/login_page.py
