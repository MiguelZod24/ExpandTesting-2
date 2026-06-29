Diagnóstico: El problema surge porque al invocar el método 'navegar', no se estaba incluyendo correctamente el BASE_URL completo configurado en la clase. Esto resulta en un error al intentar acceder a la URL. La corrección incluye la concatenación del BASE_URL con la ruta '/login' dentro del método 'navegar'.
Archivo: pages/login_page.py
