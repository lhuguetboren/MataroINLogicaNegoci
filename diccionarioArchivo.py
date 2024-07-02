import json


# Función para guardar el diccionario en un archivo
def guardar_diccionario(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(diccionario, archivo, indent=4)
    print(f'Diccionario guardado en {nombre_archivo}')

# Función para recuperar el diccionario desde un archivo
def recuperar_diccionario(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        diccionario = json.load(archivo)
    print(f'Diccionario recuperado de {nombre_archivo}')
    return diccionario

'''# Uso de las funciones
nombre_archivo = 'assets/servidor/alojamientos.json'

#guardar_diccionario(alojamientos, nombre_archivo)
alojamientos = recuperar_diccionario(nombre_archivo)
print(alojamientos)
nombre_archivo = 'assets/servidor/alojamientos.json'
guardar_diccionario(alojamientos, nombre_archivo)
'''