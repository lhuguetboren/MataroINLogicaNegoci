'''
Clase Usuario:

Funciones:
__init__: Inicialización del objeto.
__str__: Representación en cadena del objeto.
Técnicas:
    Referencias a Objeto: Utilizada en la creación y manipulación de objetos Usuario.

Clase Habitacion:

Funciones:
    __init__: Inicialización del objeto.
    reservar: Reserva una habitación para un usuario.
    liberar: Libera una habitación ocupada.
    __str__: Representación en cadena del objeto.
Técnicas:
    Agregación de Clase: La clase Hotel tiene una lista de objetos Habitacion.
    Gestión de Excepciones: Utilizada en los métodos reservar y liberar.
    Referencias a Objeto: Accede y manipula atributos y métodos de objetos Habitacion.

Clase abstracta Establecimiento:

Funciones:
    __init__: Inicialización del objeto.
    mostrar_informacion: Muestra información básica del establecimiento.
Técnicas:
    Herencia: Utilizada para extender funcionalidades en las subclases como Hotel.
    Polimorfismo: El método mostrar_informacion es polimórfico en las subclases.
    Clase Hotel (subclase de Establecimiento):

Funciones:
__init__: Inicialización del objeto.
    reservar_habitacion: Reserva una o varias habitaciones para un usuario.
    liberar_habitacion: Libera una o varias habitaciones ocupadas por un usuario.
    mostrar_informacion: Muestra información detallada del hotel.
Técnicas:
    Herencia: Hereda de la clase Establecimiento.
    Agregación de Clase: Tiene una lista de objetos Habitacion.
    Polimorfismo: El método mostrar_informacion es polimórfico en las subclases.

Clase HotelLujo (subclase de Hotel):

Funciones:
__init__: Inicialización del objeto.
    mostrar_informacion: Muestra información detallada del hotel de lujo.
Técnicas:
    Herencia: Hereda de la clase Hotel.
    Polimorfismo: El método mostrar_informacion es polimórfico.
    Clase HotelEconomico (subclase de Hotel):

Funciones:
__init__: Inicialización del objeto.
    mostrar_informacion: Muestra información detallada del hotel económico.
Técnicas:
    Herencia: Hereda de la clase Hotel.
    Polimorfismo: El método mostrar_informacion es polimórfico.


Clase Localidad:

Funciones:
    __init__: Inicialización del objeto.
    agregar_hotel: Agrega un hotel a la localidad.
    habitaciones_libres: Calcula el número total de habitaciones libres en todos los hoteles de la localidad.
    mostrar_hoteles: Muestra información detallada de todos los hoteles de la localidad.
Técnicas:
    Agregación de Clase: Tiene una lista de objetos Hotel.
    Referencias a Objeto: Accede y manipula atributos y métodos de objetos Hotel.

Clase SistemaHoteles:

Funciones:
    __init__: Inicialización del objeto.
    agregar_hotel: Agrega un hotel al sistema de hoteles.
    buscar_hoteles_por_categoria: Busca hoteles por categoría en todas las localidades del sistema.
    buscar_habitaciones_libres_en_localidad: Busca el número de habitaciones libres en una localidad específica.
    transferir_usuario: Transfiere un usuario de un hotel a otro.
    mostrar_hoteles: Muestra información detallada de todos los hoteles en todas las localidades del sistema.
    guardar_datos: Guarda el estado del sistema en un archivo.
    cargar_datos: Carga el estado del sistema desde un archivo.
Técnicas:
    Agregación de Clase: Tiene un diccionario de objetos Localidad.
    Referencias a Objeto: Accede y manipula atributos y métodos de objetos Hotel y Localidad.
    Gestión de Excepciones: Utilizada en métodos como transferir_usuario.
    Persistencia de Objetos: Guarda y carga el estado del sistema utilizando pickle.
'''

import pickle
from typing import List, Dict

# Excepciones personalizadas
class HotelException(Exception):
    pass

class ReservaException(HotelException):
    pass

class TransferenciaException(HotelException):
    pass
class Balconing(HotelException):
    pass
# Clase Usuario para representar a los usuarios del hotel
class Usuario:
    def __init__(self, nombre: str):
        try:
            if "smith" in nombre.lower():
                    raise Balconing
            else:
                self.nombre = nombre
        
        except Balconing:
            print( "Usuario sospechoso de Balconing")

    def __str__(self):
        return self.nombre

# Clase Habitacion para representar habitaciones de un hotel (Agregación)
class Habitacion:
    def __init__(self, numero: int):
        self.numero = numero
        self.libre = True
        self.usuario = None
        self.suite = False

    def reservar(self, usuario: Usuario):
        if not self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está reservada.")
        self.libre = False
        self.usuario = usuario

    def liberar(self):
        if self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está libre.")
        self.libre = True
        self.usuario = None

    def __str__(self):
        return f"Habitación {self.numero} - {'Libre' if self.libre else f'Ocupada por {self.usuario}'}"

#Clase abstracta--Superclase para todos los establecimientos
class Establecimiento:
    def __init__(self, nombre: str, direccion: str, localidad: str):
        self.nombre = nombre
        self.direccion = direccion
        self.localidad = localidad
    
    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Dirección: {self.direccion}")
        print(f"Localidad: {self.localidad}")

# Clase Hotel que hereda de Establecimiento
class Hotel(Establecimiento):
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int):
        super().__init__(nombre, direccion, localidad)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i) for i in range(1, num_habitaciones + 1)]
        self.usuarios: List[Usuario] = []

    def reservar_habitacion(self, usuario: Usuario, cantidad: int = 1) -> bool:
        habitaciones_libres = [hab for hab in self.habitaciones if hab.libre]
        if len(habitaciones_libres) < cantidad:
            raise ReservaException("No hay suficientes habitaciones libres.")
        
        for i in range(cantidad):
            habitaciones_libres[i].reservar(usuario)
        self.usuarios.append(usuario)
        print(f"{cantidad} habitación(es) reservada(s) en {self.nombre} por {usuario}.")
        return True

    def liberar_habitacion(self, usuario: Usuario, cantidad: int = 1) -> bool:
        habitaciones_ocupadas = [hab for hab in self.habitaciones if not hab.libre and hab.usuario == usuario]
        if len(habitaciones_ocupadas) < cantidad:
            raise ReservaException("El usuario no tiene suficientes habitaciones reservadas para liberar.")
        
        for i in range(cantidad):
            habitaciones_ocupadas[i].liberar()
        self.usuarios.remove(usuario)
        print(f"{cantidad} habitación(es) liberada(s) en {self.nombre} por {usuario}.")
        return True

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Categoría: {self.categoria} estrellas")
        print(f"Habitaciones:")
        for habitacion in self.habitaciones:
            print(f"  - {habitacion}")
        print(f"Usuarios: {', '.join(str(usuario) for usuario in self.usuarios)}")

# Subclase HotelLujo que hereda de Hotel
class HotelLujo(Hotel):
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int, num_suites: int,tiene_spa: bool, tiene_restaurante_gourmet: bool):
        super().__init__(nombre, direccion, localidad, categoria, num_habitaciones)
        self.num_suites =num_suites
        self.tiene_spa = tiene_spa
        self.tiene_restaurante_gourmet = tiene_restaurante_gourmet

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Servicios adicionales:")
        print(f"  - Spa: {self.tiene_spa}")
        print(f"  - Restaurante Gourmet: {self.tiene_restaurante_gourmet}")

# Subclase HotelSuperLujo que hereda de Hotel
class HotelSuperLujo(Hotel):
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int, num_suites: int,tiene_spa: bool, tiene_restaurante_gourmet: bool):
        super().__init__(nombre, direccion, localidad, categoria, num_habitaciones)
        self.tiene_spa = tiene_spa
        self.tiene_restaurante_gourmet = tiene_restaurante_gourmet
        for i in range(30):
            self.habitaciones[i].suite=True
        

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Servicios adicionales:")
        print(f"  - Spa: {self.tiene_spa}")
        print(f"  - Restaurante Gourmet: {self.tiene_restaurante_gourmet}")

# Nueva Subclase HotelEconomico que hereda de Hotel
class HotelEconomico(Hotel):
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int, incluye_desayuno: bool):
        super().__init__(nombre, direccion, localidad, categoria, num_habitaciones)
        self.incluye_desayuno = incluye_desayuno

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Servicios adicionales:")
        print(f"  - Desayuno: {self.incluye_desayuno}")


# Nueva Subclase HotelparaGuirisSinUnDuro(euro)
class HotelParaGuirisSinUnDuro(HotelEconomico):
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int, incluye_desayuno: bool, balconing:bool):
        super().__init__(nombre, direccion, localidad, categoria, num_habitaciones, incluye_desayuno)
        self.balconing=balconing
    
    def mostrar_informacion(self):
        #super().mostrar_informacion()
        print(f"sin desayuno pero con balconing")
        print(f"  - balconing: {self.balconing}")


# Clase Localidad para gestionar información de localidades
class Localidad:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hoteles: List[Hotel] = []

    def agregar_hotel(self, hotel: Hotel):
        self.hoteles.append(hotel)
        print(f"Hotel {hotel.nombre} agregado a la localidad {self.nombre}.")

    def habitaciones_libres(self) -> int:
        total_habitaciones_libres = sum(hab.libre for hotel in self.hoteles for hab in hotel.habitaciones)
        return total_habitaciones_libres

    def mostrar_hoteles(self):
        print(f"Hoteles en {self.nombre}:")
        for hotel in self.hoteles:
            hotel.mostrar_informacion()
            print()

# Sistema de gestión de hoteles y localidades
class SistemaHoteles:
    def __init__(self):
        self.localidades: Dict[str, Localidad] = {}

    def agregar_hotel(self, hotel: Hotel):
        if hotel.localidad not in self.localidades:
            self.localidades[hotel.localidad] = Localidad(hotel.localidad)
        self.localidades[hotel.localidad].agregar_hotel(hotel)
        print(f"Hotel {hotel.nombre} agregado al sistema en la localidad {hotel.localidad}.")
#Referencias a Objeto:

    def buscar_hoteles_por_categoria(self, categoria: int) -> List[Hotel]:
        hoteles_filtrados = []
        for localidad in self.localidades.values():
            hoteles_filtrados.extend([hotel for hotel in localidad.hoteles if hotel.categoria == categoria])
        return hoteles_filtrados
#Referencias a Objeto:
    def buscar_habitaciones_libres_en_localidad(self, nombre_localidad: str) -> int:
        if nombre_localidad in self.localidades:
            return self.localidades[nombre_localidad].habitaciones_libres()
        else:
            return 0
#enlace dinamico
    def transferir_usuario(self, usuario: Usuario, hotel_origen: Hotel, hotel_destino: Hotel) -> bool:
        try:
            hotel_origen.liberar_habitacion(usuario)
            hotel_destino.reservar_habitacion(usuario)
            print(f"Usuario {usuario} transferido de {hotel_origen.nombre} a {hotel_destino.nombre}.")
            return True
        except (ReservaException, TransferenciaException) as e:
            print(f"No se pudo transferir al usuario {usuario}: {e}")
            return False

    def mostrar_hoteles(self):
        for localidad in self.localidades.values():
            localidad.mostrar_hoteles()

    def guardar_datos(self, archivo: str):
        with open(archivo, 'wb') as f:
            pickle.dump(self, f)
        print(f"Datos guardados en {archivo}.")

    @staticmethod
    def cargar_datos(archivo: str):
        with open(archivo, 'rb') as f:
            sistema = pickle.load(f)
        print(f"Datos cargados desde {archivo}.")
        return sistema

# Ejemplo de uso
if __name__ == "__main__":
    sistema = SistemaHoteles()

    '''hotel1 = Hotel("Hotel Central", "Calle Principal 123", "Ciudad A", 5, 100)
    hotel2 = Hotel("Hotel Económico", "Avenida Secundaria 456", "Ciudad A", 3, 50)
    hotel3 = Hotel("Hotel Playa", "Calle del Mar 789", "Ciudad B", 4, 75)
    hotel4 = HotelLujo("Hotel Lujo", "Avenida del Lujo 1", "Ciudad A", 5, 50, tiene_spa=True, tiene_restaurante_gourmet=True)
    hotel5 = HotelEconomico("Hotel Económico Plus", "Calle Ahorro 10", "Ciudad C", 2, 80, incluye_desayuno=True)'''
    hotel6= HotelParaGuirisSinUnDuro("Hotel Económico Plus", "Calle Ahorro 10", "Ciudad C", 2, 80, incluye_desayuno=True, balconing=True)

    '''sistema.agregar_hotel(hotel1)
    sistema.agregar_hotel(hotel2)
    sistema.agregar_hotel(hotel3)
    sistema.agregar_hotel(hotel4)
    sistema.agregar_hotel(hotel5)'''
    sistema.agregar_hotel(hotel6)

    usuario1 = Usuario("Juan Perez")
    usuario2 = Usuario("Jhon Smith")

    try:
        hotel6.reservar_habitacion(usuario1, 2)
        hotel6.reservar_habitacion(usuario2, 1)
    except ReservaException as e:
        print(f"Error en la reserva: {e}")
    
    sistema.mostrar_hoteles()
    
    # Polimorfismo y Enlace Dinámico
    '''hoteles = [hotel1, hotel4, hotel5,hotel6]  # Lista de diferentes tipos de hoteles
    for hotel in hoteles:
        hotel.mostrar_informacion()
        print("---")

    print("Transferir usuario:")
    sistema.transferir_usuario(usuario1, hotel1, hotel4)

    sistema.mostrar_hoteles()

    # Guardar datos
    sistema.guardar_datos('sistema_hoteles.pkl')

    # Cargar datos
    sistema_cargado = SistemaHoteles.cargar_datos('sistema_hoteles.pkl')
    sistema_cargado.mostrar_hoteles()'''
