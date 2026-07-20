Diagnóstico: El principal error identificado en el test se debe a que el assertion falla intencionalmente porque el mensaje de error buscado ('Este mensaje nunca aparecerá') no coincide con el texto que realmente aparece en la página tras un login exitoso ('You logged into a secure area!'). Este comportamiento parece ser intencional para verificar la captura de artefactos como capturas de pantalla y trazas del test fallido.

Además, se realizaron correcciones menores en los selectores para hacerlos más robustos y evitar posibles conflictos, eliminando por ejemplo el uso de `input[name='...']` a favor de `[name='...']`.

Se mejoró la validación del método `campo_vacio` para manejar casos en los que el valor del campo sea `None` o esté vacío (solo espacios). También se agregó `wait_for_selector` en `valor_ingresado` para garantizar que el campo esté disponible antes de solicitar su valor actual.
Archivo: pages/login_page.py
