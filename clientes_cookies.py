import json
import random
import diccionarioArchivo

clientes_diccionario = {
    "datos_clientes": [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "email": "juan.perez@example.com",
            "preferencias_viaje": [
                "Calella",
                "Mataró",
                "Arenys de Mar"
            ],
            "inputs": {
                "Campo de búsqueda": 5,
                "Botón de reserva": 3,
                "Selector de fechas": 2,
                "Campo de comentarios": 1
            },
            "cookies": {
                "pais": "España",
                "hora": "15:30",
                "dispositivo": "Móvil",
                "compra": False
            }
        },
        {
            "id": 2,
            "nombre": "María García",
            "email": "maria.garcia@example.com",
            "preferencias_viaje": [
                "Malgrat de Mar",
                "Canet de Mar",
                "Sant Pol de Mar"
            ],
            "inputs": {
                "Opciones de pago": 2,
                "Botón de suscripción a boletín": 1,
                "Número de personas": 4,
                "Botón de búsqueda": 3
            },
            "cookies": {
                "pais": "España",
                "hora": "10:45",
                "dispositivo": "Ordenador",
                "compra": True
            }
        },
        {
            "id": 3,
            "nombre": "Carlos López",
            "email": "carlos.lopez@example.com",
            "preferencias_viaje": [
                "Pineda de Mar",
                "Premià de Mar",
                "Calella"
            ],
            "inputs": {
                "Checkbox de preferencias": 2,
                "Campo de búsqueda": 7,
                "Botón de enviar formulario": 1,
                "Campo de comentarios": 2
            },
            "cookies": {
                "pais": "España",
                "hora": "12:15",
                "dispositivo": "Tableta",
                "compra": False
            }
        },
        {
            "id": 4,
            "nombre": "Ana Martínez",
            "email": "ana.martinez@example.com",
            "preferencias_viaje": [
                "Mataró",
                "Malgrat de Mar",
                "Arenys de Mar"
            ],
            "inputs": {
                "Selector de fechas": 3,
                "Número de personas": 5,
                "Botón de reserva": 4,
                "Campo de búsqueda": 6
            },
            "cookies": {
                "pais": "España",
                "hora": "18:00",
                "dispositivo": "Ordenador",
                "compra": True
            }
        }
    ]
}

def generate_random_time():
    hora = random.randint(0, 23)
    minutos = random.randint(0, 59)
    segundos = random.randint(0, 59)
    return f"{hora:02d}:{minutos:02d}:{segundos:02d}"

def set_cookie_with_random_timestamp(localidad):
    hora_conexion = generate_random_time()
    return {localidad: hora_conexion}

# Lista de localidades (países) del mundo
localidades = ["Argentina", "España", "Francia", "Estados Unidos", "China"]

# Diccionario para almacenar los resultados
cookies_dict = {}

# Bucle para invocar la función para cada localidad y almacenar los resultados en el diccionario
for localidad in localidades:
    cookies_dict.update(set_cookie_with_random_timestamp(localidad))


diccionarioArchivo.guardar_diccionario(cookies_dict,"MataroIN/servidor/cookies.json")
#Estadisticas sobre la informacion



def estadisticas_clientes ():
    informacion=diccionarioArchivo.recuperar_diccionario("MataroIN/servidor/datos_clientes.json")
    for dato in informacion.get("datos_clientes"):
        for clave, valor in dato.items():
            if clave == "preferencias_viaje":
                for clave_viajes in valor:
                    if clave_viajes in clave:
                        #dar valor a las palabras de preferencias viajes para despues ordenarlas
                        print(clave_viajes)

estadisticas_clientes()