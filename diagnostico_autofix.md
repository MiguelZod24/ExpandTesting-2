Diagnóstico: El error principal fue un TimeoutError al intentar navegar a la URL del login. Esto ocurrió porque el tiempo límite predeterminado (30 segundos) para la navegación se excedió. Esto podría deberse a la lentitud de la carga del sitio web o demoras en la red. La solución fue aumentar el tiempo de espera (timeout) a 60 segundos en la función `navegar`.
Archivo: pages/login_page.py
