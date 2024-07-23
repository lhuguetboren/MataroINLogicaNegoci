import asyncio
import json
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime
hola
# Configuración base de SQLAlchemy
Base = declarative_base()

# Definición de la clase Evento
class Evento(Base):
    __tablename__ = 'eventos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, nullable=False)
    opcion = Column(Integer, nullable=False)
    texto = Column(Text, nullable=False)

# Crear el engine de manera asíncrona
DATABASE_URL = "mysql+aiomysql://flask:flask2024@localhost/mataroin"
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Función para crear la sesión de SQLAlchemy de manera asíncrona
async def create_async_session():
    async_session = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
    return async_session

# Definición de la clase Pila
class Pila:
    def __init__(self):
        self.elementos = []
        self.next_id = 1  # Inicializamos un contador para los IDs de los eventos
        self.datos_uber = {}  # Diccionario para almacenar datos enviados a Uber

    def desapilar_por_id(self, id_evento):
        for i, evento in enumerate(self.elementos):
            if evento['id'] == id_evento:
                return self.elementos.pop(i)
        print("No se encontró ningún evento con el ID especificado.")
        return None
    
    async def push(self, id_cliente, opcion, elemento):
        evento = {
            "id": self.next_id,
            "elemento": elemento
        }
        self.elementos.append(evento)
        self.next_id += 1

        # Guardar evento en la base de datos de manera asíncrona
        async_session = await create_async_session()
        async with async_session() as session:
            nuevo_evento = Evento(
                id_cliente=id_cliente,  # Pasar el ID correcto del cliente
                opcion=opcion,
                texto=elemento
            )
            session.add(nuevo_evento)
            await session.commit()
            print("Evento añadido a la base de datos con ID:", nuevo_evento.id)

    def pop(self):
        if self.is_empty():
            print("La pila está vacía.")
            return None
        return self.elementos.pop()
    
    def peek(self):
        if self.is_empty():
            print("La pila está vacía.")
            return None
        return self.elementos[-1]
    
    def size(self):
        return len(self.elementos)
    
    def is_empty(self):
        return self.size() == 0

    async def enviar_datos_uber(self, id_cliente, cliente, lugar_recogida, lugar_destino):
        # Simular respuesta JSON de Uber con conductores asignados
        await asyncio.sleep(2)  # Simulación de operación asíncrona
        conductores_asignados = [
            {"nombre": "Conductor 1", "vehiculo": "Toyota Prius"},
            {"nombre": "Conductor 2", "vehiculo": "Honda Civic"}
        ]
        self.datos_uber["conductores_asignados"] = conductores_asignados

        fecha_reserva = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = {
            "cliente": cliente,
            "fecha_reserva": fecha_reserva,
            "lugar_recogida": lugar_recogida,
            "lugar_destino": lugar_destino,
            "empresa": "Uber"
        }
        await self.push(id_cliente, 5, json.dumps(evento))

    async def evento_conductor(self, id_cliente, estado):
        eventos_validos = ["en camino", "recogiendo", "entregado"]
        if estado.lower() in eventos_validos:
            evento = {
                "estado": estado.lower(),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            await self.push(id_cliente, 7, json.dumps(evento))
        else:
            print("Estado no válido. Los estados válidos son 'en camino', 'recogiendo' o 'entregado'.")

    def responder_datos_uber(self):
        if "conductores_asignados" in self.datos_uber:
            conductores = self.datos_uber["conductores_asignados"]
            print("Conductores asignados por Uber:")
            for conductor in conductores:
                print(f"Nombre: {conductor['nombre']}")
                print(f"Vehículo: {conductor['vehiculo']}")
                print("-----------------------------")
        else:
            print("No se encontraron datos de conductores asignados por Uber.")

    def mostrar_elementos(self):
        if self.is_empty():
            print("La pila está vacía.")
        else:
            print("Elementos en la pila:")
            for evento in self.elementos:
                print(f"ID: {evento['id']}")
                print(f"Texto: {evento['elemento']}")
                print("-----------------------------")

# Función para mostrar el menú de opciones
def mostrar_menu():
    print("\nCREADOR DE PILAS. ¿Qué quiere hacer?")
    print("0. Salir")
    print("1. Apilar")
    print("2. Desapilar")
    print("3. Mostrar número de elementos")
    print("5. Enviar datos a Uber")
    print("6. Responder datos de Uber")
    print("7. Evento del conductor")

# Función para pedir la opción al usuario
def pedir_opcion():
    opcion = -1
    while opcion < 0 or opcion > 7:
        try:
            opcion = input("Ingrese la opción (0-7): ").strip()  # Eliminar espacios en blanco al inicio y final
            if opcion == '':
                raise ValueError("No se ingresó ninguna opción.")
            opcion = int(opcion)
            if opcion < 0 or opcion > 7:
                raise ValueError("Opción fuera de rango.")
        except ValueError as e:
            print(f"Error: {e} Intente nuevamente.")
    return opcion

# Función para ejecutar la acción según la opción elegida
async def hacer_accion(opcion, pila):
    if opcion == 1:
        id_cliente = int(input("Ingrese el ID del cliente: "))
        elemento = input("Ingrese el elemento a apilar: ")
        await pila.push(id_cliente, opcion, elemento)
        print("Elemento apilado y guardado en la base de datos correctamente.")
    elif opcion == 2:
        id_evento = int(input("Ingrese el ID del evento que desea desapilar: "))
        # Lógica para desapilar el evento con el ID especificado
        elemento_desapilado = pila.desapilar_por_id(id_evento)
        if elemento_desapilado:
            print("Elemento desapilado:", elemento_desapilado)
    elif opcion == 3:
        pila.mostrar_elementos()  # Mostrar los detalles de los elementos en la pila
    elif opcion == 5:
        pila.mostrar_elementos()  # Mostrar los detalles de los elementos en la pila
    elif opcion == 6:
        pila.responder_datos_uber()
    elif opcion == 7:
        id_cliente = int(input("Ingrese el ID del cliente: "))
        estado = input("¿Qué estado desea reportar? (en camino/recogiendo/entregado): ")
        await pila.evento_conductor(id_cliente, estado)
    elif opcion == 0:
        print("Saliendo del programa...")
    else:
        print("Opción no válida.")

# Función principal para ejecutar el programa
async def main():
    # Crear la instancia de la pila
    pila = Pila()
    
    while True:
        mostrar_menu()
        opcion = pedir_opcion()
        if opcion == 0:
            break
        await hacer_accion(opcion, pila)
        input("Presione ENTER para continuar...")

if __name__ == "__main2__":
    # Ejecutar el programa principal de manera asíncrona
    print("Iniciando el programa...")
    asyncio.run(main())
    print("Programa finalizado.")


alta_cliente = {
    "id_cliente": 123,
    "fecha": "2024-07-11 10:00:00"  # Fecha en la que se realiza el alta del cliente
}

enviar_uber = {
    "id_cliente": 123,
    "cliente": "Nombre del cliente",
    "lugar_recogida": "Dirección de recogida",
    "lugar_destino": "Dirección de destino",
    "fecha": "2024-07-11 10:15:00"  # Fecha en la que se envían los datos a Uber
}

respuesta_uber = {
    "conductores_asignados": [
        {"nombre": "Conductor 1", "vehiculo": "Toyota Prius", "estado": "en camino"},
        {"nombre": "Conductor 2", "vehiculo": "Honda Civic", "estado": "recogiendo"}
    ],
    "fecha": "2024-07-11 10:30:00"  # Fecha en la que se recibe la respuesta de Uber
}


conductor_en_marcha = {
    "nombre_conductor": "Conductor 1",
    "vehiculo": "Toyota Prius",
    "estado": "en camino",  # Estado actual del conductor: en camino / recogiendo / entregado
    "fecha": "2024-07-11 11:00:00"  # Fecha en la que se reporta el estado del conductor
}

conductor_recogido = {
    "nombre_conductor": "Conductor 1",
    "vehiculo": "Toyota Prius",
    "estado": "recogiendo",  # Estado actual del conductor: en camino / recogiendo / entregado
    "fecha": "2024-07-11 11:15:00"  # Fecha en la que se reporta el estado del conductor
}

conductor_entregado = {
    "nombre_conductor": "Conductor 1",
    "vehiculo": "Toyota Prius",
    "estado": "entregado",  # Estado actual del conductor: en camino / recogiendo / entregado
    "fecha": "2024-07-11 11:30:00"  # Fecha en la que se reporta el estado del conductor
}


