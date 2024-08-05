def js_to_css_string(js_file_path):
    try:
        with open(js_file_path, 'r') as file:
            js_code = file.read()

        # Reemplazar caracteres especiales de CSS
        css_string = js_code.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

        # Agregar comillas
        css_string = '"' + css_string + '"'

        return css_string

    except FileNotFoundError:
        return None

if __name__ == "__main__":
    js_file_path = input("Ingrese la ruta del archivo JavaScript: ")
    css_string = js_to_css_string(js_file_path)
    if css_string:
        print("Cadena CSS generada:")
        print(css_string)
    else:
        print("El archivo no fue encontrado.")
