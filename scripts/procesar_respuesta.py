import json
import sys

def main():
    response = sys.stdin.read()
    try:
        data = json.loads(response)
        content = data['choices'][0]['message']['content']
        # Limpia bloques markdown si los hay
        clean = content.replace('```json', '').replace('```', '').strip()
        parsed = json.loads(clean)
        diagnostico = parsed.get('diagnostico', 'No disponible')
        archivo = parsed.get('archivo', 'pages/login_page.py')
        codigo = parsed.get('codigo_completo_corregido', '')
        print(f"Diagnóstico: {diagnostico}")
        print(f"Archivo: {archivo}")
        # Guarda el código corregido
        with open('codigo_corregido.py', 'w') as f:
            f.write(codigo)
        # Guarda el archivo destino
        with open('archivo_destino.txt', 'w') as f:
            f.write(archivo)
    except Exception as e:
        print(f"Error procesando respuesta: {e}")
        print(f"Response raw: {response[:500]}")

if __name__ == '__main__':
    main()
