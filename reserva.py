import pickle
from typing import List, Dict

# Excepciones personalizadas
class HotelException(Exception):
    """
    Excepción base para errores relacionados con el hotel.
    """
    pass

class ReservaException(HotelException):
    """
    Excepción para errores en reservas de habitaciones.
    """
    pass

class TransferenciaException(HotelException):
    """
    Excepción para errores en transferencias de usuarios entre hoteles.
    """
    pass

class BalconingException(Exception):
    """
    Excepción específica para usuarios identificados por hacer balconing.

    :param mensaje: Mensaje de la excepción.
    """
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

class Usuario:
    """
    Clase que representa a los usuarios del hotel.

    :param nombre: Nombre del usuario.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Habitacion:
    """
    Clase que representa una habitación de hotel.

    :param numero: Número de la habitación.
    :param es_suite: Indica si la habitación es una suite.
    """
    def __init__(self, numero: int, es_suite: bool = False):
        self.numero = numero
        self.libre = True
        self.usuario = None
        self.es_suite = es_suite

    def reservar(self, usuario: Usuario):
        """
        Reserva la habitación para un usuario.

        :param usuario: Usuario que reserva la habitación.
        :raises BalconingException: Si el usuario ha sido identificado por hacer balconing.
        :raises ReservaException: Si la habitación ya está reservada.
        """
        if "Smith" in usuario.nombre:
            raise BalconingException(f"El usuario {usuario} ha sido identificado por hacer balconing.")
        if not self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está reservada.")
        self.libre = False
        self.usuario = usuario

    def liberar(self):
        """
        Libera la habitación.

        :raises ReservaException: Si la habitación ya está libre.
        """
        if self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está libre.")
        self.libre = True
        self.usuario = None

    def __str__(self):
        tipo_habitacion = 'Suite' if self.es_suite else 'Habitación'
        estado = 'Libre' if self.libre else f'Ocupada por {self.usuario}'
        return f"{tipo_habitacion} {self.numero} - {estado}"

class Establecimiento:
    """
    Clase base para representar un establecimiento.

    :param nombre: Nombre del establecimiento.
    :param direccion: Dirección del establecimiento.
    :param localidad: Localidad del establecimiento.
    """
    def __init__(self, nombre: str, direccion: str, localidad: str):
        self.nombre = nombre
        self.direccion = direccion
        self.localidad = localidad
    
    def mostrar_informacion(self):
        """
        Muestra la información del establecimiento.
        """
        print(f"Nombre: {self.nombre}")
        print(f"Dirección: {self.direccion}")
        print(f"Localidad: {self.localidad}")

class Hotel(Establecimiento):
    """
    Clase que representa un hotel.

    :param nombre: Nombre del hotel.
    :param direccion: Dirección del hotel.
    :param localidad: Localidad del hotel.
    :param categoria: Categoría del hotel (estrellas).
    :param num_habitaciones: Número de habitaciones del hotel.
    """
    def __init__(self, nombre: str, direccion: str, localidad: str, categoria: int, num_habitaciones: int):
        super().__init__(nombre, direccion, localidad)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i, es_suite=(i <= 30)) for i in range(1, num_habitaciones + 1)]
        self.usuarios: List[Usuario] = []

    def reservar_habitacion(self, usuario: Usuario, cantidad: int = 1) -> bool:
        """
        Reserva una o más habitaciones para un usuario.

        :param usuario: Usuario que reserva la(s) habitación(es).
        :param cantidad: Número de habitaciones a reservar.
        :raises ReservaException: Si no hay suficientes habitaciones libres.
        :return: True si la reserva se realizó correctamente.
        """
        habitaciones_libres = [hab for hab in self.habitaciones if hab.libre]
        if len(habitaciones_libres) < cantidad:
            raise ReservaException("No hay suficientes habitaciones libres.")
        
        for i in range(cantidad):
            habitaciones_libres[i].reservar(usuario)
        self.usuarios.append(usuario)
        print(f"{cantidad} habitación(es) reservada(s) en {self.nombre} por {usuario}.")
        return True

    def liberar_habitacion(self, usuario: Usuario, cantidad: int = 1) -> bool:
        """
        Libera una o más habitaciones reservadas por un usuario.

        :param usuario: Usuario que libera la(s) habitación(es).
        :param cantidad: Número de habitaciones a liberar.
        :raises ReservaException: Si el usuario no tiene suficientes habitaciones reservadas para liberar.
        :return: True si la liberación se realizó correctamente.
        """
        habitaciones_ocupadas = [hab for hab in self.habitaciones if not hab.libre and hab.usuario == usuario]
        if len(habitaciones_ocupadas) < cantidad:
            raise ReservaException("El usuario no tiene suficientes habitaciones reservadas para liberar.")
        
        for i in range(cantidad):
            habitaciones_ocupadas[i].liberar()
        self.usuarios.remove(usuario)
        print(f"{cantidad} habitación(es) liberada(s) en {self.nombre} por {usuario}.")
        return True
    
    def reservar_suite(self, usuario: Usuario, cantidad: int = 1) -> bool:
        """
        Reserva una o más suites para un usuario.

        :param usuario: Usuario que reserva la(s) suite(s).
        :param cantidad: Número de suites a reservar.
        :raises ReservaException: Si no hay suficientes suites libres.
        :return: True si la reserva se realizó correctamente.
        """
        habitaciones_suite_libres = [hab for hab in self.habitaciones if hab.libre and hab.es_suite]
        if len(habitaciones_suite_libres) < cantidad:
            raise ReservaException("No hay suficientes suites libres.")
        
        for i in range(cantidad):
            for habitacion in habitaciones_suite_libres:
                if habitacion.libre and habitacion.es_suite:
                    habitacion.reservar(usuario)
                    break 
        
        self.usuarios.append(usuario)
        print(f"{cantidad} suite(s) reservada(s) en {self.nombre} por {usuario}.")
        return True
       
    def mostrar_suites(self):
        """
        Muestra todas las suites disponibles en el hotel.
        """
        print("Suites disponibles:")
        for habitacion in self.habitaciones:
            if habitacion.es_suite:
                print(habitacion)

    def mostrar_informacion(self):
        """
        Muestra la información del hotel.
        """
        super().mostrar_informacion()
        print(f"Categoría: {self.categoria} estrellas")
        print(f"Habitaciones:")
        for habitacion in self.habitaciones:
            print(f"  - {habitacion}")
        print(f"Usuarios: {', '.join(str(usuario) for usuario in self.usuarios)}")

class Localidad:
    """
    Clase para gestionar información de localidades.

    :param nombre: Nombre de la localidad.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hoteles: List[Hotel] = []

    def agregar_hotel(self, hotel: Hotel):
        """
        Agrega un hotel a la localidad.

        :param hotel: Hotel a agregar.
        """
        self.hoteles.append(hotel)
        print(f"Hotel {hotel.nombre} agregado a la localidad {self.nombre}.")

    def habitaciones_libres(self) -> int:
        """
        Devuelve el número total de habitaciones libres en la localidad.

        :return: Número total de habitaciones libres.
        """
        total_habitaciones_libres = sum(hab.libre for hotel in self.hoteles for hab in hotel.habitaciones)
        return total_habitaciones_libres

    def mostrar_hoteles(self):
        """
        Muestra la información de todos los hoteles en la localidad.
        """
        print(f"Hoteles en {self.nombre}:")
        for hotel in self.hoteles:
            hotel.mostrar_informacion()
            print()

class SistemaHoteles:
    """
    Sistema de gestión de hoteles y localidades.
    """
    def __init__(self):
        self.localidades: Dict[str, Localidad] = {}

    def agregar_hotel(self, hotel: Hotel):
        """
        Agrega un hotel al sistema.

        :param hotel: Hotel a agregar.
        """
        if hotel.localidad not in self.localidades:
            self.localidades[hotel.localidad] = Localidad(hotel.localidad)
        self.localidades[hotel.localidad].agregar_hotel(hotel)
        print(f"Hotel {hotel.nombre} agregado al sistema en la localidad {hotel.localidad}.")

    def buscar_hoteles_por_categoria(self, categoria: int) -> List[Hotel]:
        """
        Busca hoteles por su categoría.

        :param categoria: Categoría de los hoteles a buscar.
        :return: Lista de hoteles que coinciden con la categoría.
        """
        hoteles_filtrados = []
        for localidad in self.localidades.values():
            hoteles_filtrados.extend([hotel for hotel in localidad.hoteles if hotel.categoria == categoria])
        return hoteles_filtrados

    def buscar_habitaciones_libres_en_localidad(self, nombre_localidad: str) -> int:
        """
        Busca el número de habitaciones libres en una localidad.

        :param nombre_localidad: Nombre de la localidad a buscar.
        :return: Número de habitaciones libres en la localidad.
        """
        if nombre_localidad in self.localidades:
            return self.localidades[nombre_localidad].habitaciones_libres()
        else:
            return 0

    def transferir_usuario(self, usuario: Usuario, hotel_origen: Hotel, hotel_destino: Hotel) -> bool:
        """
        Transfiere un usuario de un hotel a otro.

        :param usuario: Usuario a transferir.
        :param hotel_origen: Hotel de origen.
        :param hotel_destino: Hotel de destino.
        :raises ReservaException: Si ocurre un error al liberar o reservar la habitación.
        :raises TransferenciaException: Si ocurre un error en la transferencia.
        :return: True si la transferencia se realizó correctamente.
        """
        try:
            hotel_origen.liberar_habitacion(usuario)
            hotel_destino.reservar_habitacion(usuario)
            print(f"Usuario {usuario} transferido de {hotel_origen.nombre} a {hotel_destino.nombre}.")
            return True
        except (ReservaException, TransferenciaException) as e:
            print(f"No se pudo transferir al usuario {usuario}: {e}")
            return False

    def mostrar_hoteles(self):
        """
        Muestra la información de todos los hoteles en el sistema.
        """
        for localidad in self.localidades.values():
            localidad.mostrar_hoteles()

    def guardar_datos(self, archivo: str):
        """
        Guarda los datos del sistema en un archivo.

        :param archivo: Nombre del archivo donde guardar los datos.
        """
        with open(archivo, 'wb') as f:
            pickle.dump(self, f)
        print(f"Datos guardados en {archivo}.")

    @staticmethod
    def cargar_datos(archivo: str):
        """
        Carga los datos del sistema desde un archivo.

        :param archivo: Nombre del archivo desde donde cargar los datos.
        :return: Instancia del sistema cargado.
        """
        with open(archivo, 'rb') as f:
            sistema = pickle.load(f)
        print(f"Datos cargados desde {archivo}.")
        return sistema

# Ejemplo de uso
if __name__ == "__main__":
    sistema = SistemaHoteles()

    hotel3 = Hotel("Hotel Playa", "Calle del Mar 789", "Ciudad B", 4, 75)
    sistema.agregar_hotel(hotel3)

    usuario1 = Usuario("Juan Perez")
    usuario2 = Usuario("Ana Gomez")
    usuario3 = Usuario("Pau Smith")

    sistema.mostrar_hoteles()
    try:
        hotel3.reservar_habitacion(usuario3, 1)
        print(f"Reserva exitosa para {usuario3}")
    except BalconingException as e:
        print(e)
