import asyncio
import json
from datetime import datetime
import time
import os
import socket
from flask import jsonify
import pydoc

class Pila:
    """
    Clase que representa una pila para gestionar eventos.
    """

    def __init__(self):
        """
        Inicializa la pila.
        """
        self.elementos = []
        self.next_id = 1

    def desapilar_por_id(self, id_evento):
        """
        Desapila un evento por su ID.

        :param id_evento: ID del evento a desapilar.
        :return: El evento desapilado o None si no se encuentra el evento.
        """
        for i in enumerate(self.elementos):
            return self.elementos.pop(i)
        print("No se encontró ningún evento con el ID especificado.")
        return None

    async def push(self, datos):
        """
        Apila un nuevo evento de manera asíncrona.

        :param datos: Datos del evento a apilar.
        """
        evento = {
            "id": self.next_id,
            "elemento": datos
        }
        self.elementos.append(evento)
        self.next_id += 1

    def pop(self):
        """
        Desapila el último evento de la pila.

        :return: El evento desapilado o None si la pila está vacía.
        """
        if self.is_empty():
            print("La pila está vacía.")
            return None
        return self.elementos.pop()
    
    def peek(self):
        """
        Devuelve el último evento de la pila sin desapilarlo.

        :return: El último evento de la pila o None si la pila está vacía.
        """
        if self.is_empty():
            print("La pila está vacía.")
            return None
        return self.elementos[-1]
    
    def size(self):
        """
        Devuelve el número de eventos en la pila.

        :return: Número de eventos en la pila.
        """
        return len(self.elementos)
    
    def is_empty(self):
        """
        Verifica si la pila está vacía.

        :return: True si la pila está vacía, False en caso contrario.
        """
        return self.size() == 0

    async def afegir(self, id, datos):
        """
        Añade un nuevo evento a la pila después de un retraso simulado.

        :param id: ID del evento.
        :param datos: Datos del evento a añadir.
        """
        await asyncio.sleep(2)
        await self.push(json.dumps(datos))

    def mostrar_elementos(self):
        """
        Muestra los elementos de la pila y los envía a través de un socket.
        """
        if self.is_empty():
            data = "La pila está vacía."
        else:
            data = "Elementos en la pila:\n"
            for evento in self.elementos:
                data += f"ID: {evento['id']}\n"
                data += f"Elemento: {evento['elemento']}\n"
                data += "-----------------------------\n"

        host = '127.0.0.1'  # IP del servidor de socket
        port = 65432  # Puerto del servidor de socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            while True:
                s.sendall(data.encode('utf-8'))
                print(f"Enviado: {data}")
                time.sleep(5)

async def procesar_acciones(pila, acciones):
    """
    Procesa una lista de acciones y las añade a la pila.

    :param pila: Instancia de la clase Pila.
    :param acciones: Lista de acciones a procesar.
    """
    for accion in acciones:
        opcion = accion.get("opcion")
        if opcion is not None:
            await pila.afegir(accion["id"], accion)
        else:
            print("Opción no válida en el archivo.")

async def leer_archivo_datos(pila, archivo="pila.json"):
    """
    Lee las acciones desde un archivo JSON y las procesa.

    :param pila: Instancia de la clase Pila.
    :param archivo: Nombre del archivo JSON a leer.
    """
    while True:
        if os.path.exists(archivo):
            with open(archivo, "r") as file:
                try:
                    acciones = json.load(file)
                    await procesar_acciones(pila, acciones)
                    eliminar_archivo(archivo)
                except json.JSONDecodeError as e:
                    print(f"Error al leer el archivo JSON: {e}")
        else:
            pila.mostrar_elementos()
        await asyncio.sleep(5)  # Esperar 5 segundos antes de verificar el archivo nuevamente

def eliminar_archivo(archivo):
    """
    Elimina un archivo del sistema de archivos.

    :param archivo: Nombre del archivo a eliminar.
    """
    if os.path.exists(archivo):
        os.remove(archivo)
        print(f"Archivo '{archivo}' eliminado.")
    else:
        print(f"El archivo '{archivo}' no existe.")

async def main():
    """
    Función principal que inicializa la pila y lee las acciones desde un archivo.
    """
    pila = Pila()
    await leer_archivo_datos(pila)

if __name__ == "__main__":
    print("Iniciando el programa...")
    asyncio.run(main())
    print("Programa finalizado.")
