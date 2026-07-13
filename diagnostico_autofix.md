Diagnóstico: El error ocurre porque el test evalúa que el mensaje esperado ('Este mensaje nunca aparecerá') no coincide con el mensaje real retornado por la aplicación ('You logged into a secure area!'). Esto provocó que la validación assert falle, lo cual es intencional según el diseño del test para verificar la captura de artefactos en caso de errores.
Archivo: pages/login_page.py
