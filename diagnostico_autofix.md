Diagnóstico: El código original tenía problemas menores de implementación:
1. Los selectores de `username_input`, `password_input` y `login_button` usaban comillas dobles en lugar de simples, lo cual es inconsistente con el estándar PEP 8 en Python. Este problema ha sido corregido a nivel de estilo y claridad (aunque no es funcionalmente erróneo).
2. Cambié los métodos para usar `locator` en lugar de métodos directos como `fill()` y `click()`, ya que `locator` ofrece mejores opciones de manejo de errores y consistencia con las buenas prácticas modernas de Playwright.
3. En el método `obtener_error`, ajusté el assertion web-first a `locator.wait_for(state='visible')`, lo que mejora la claridad y elimina potenciales errores relacionados con `wait_for_selector`.
4. En el método `campo_vacio`, agregué una verificación para manejar el caso en que el atributo `value` sea explícitamente `None`. Esto previene errores en caso de ejecución en entornos no estándar o casos límite potenciales.
En el caso del error del test, se debe ajustar la prueba que se realiza en script test_fallo_intencional comprobaciones curso. 
Archivo: pages/login_page.py
