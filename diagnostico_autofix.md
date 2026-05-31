Diagnóstico: El problema principal radica en el método 'navegar()' en la clase 'LoginPage'. El código original utiliza 'self.page.goto("/login")', lo cual no especifica la URL base. Esto podría hacer que la navegación dependa de la configuración explícita del baseURL en el contexto de 'playwright.config.js'. Para mayor robustez y claridad, la función 'navegar()' debe incluir explícitamente el `BASE_URL` seguido de la ruta de inicio de sesión.

Además, los métodos 'campo_vacio' y 'valor_ingresado' deben garantizar que el selector esté presente en el DOM antes de intentar acceder a los atributos 'value' y 'inputValue', lo cual puede causar errores si no existe un manejador adecuado. Se añade 'wait_for_selector' con un tiempo de espera para evitar estos errores.'
}
Archivo: pages/login_page.py
