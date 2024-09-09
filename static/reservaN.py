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

class Usuario:
    """
    Clase que representa a los usuarios del hotel.

    :param id_usuario: ID único del usuario.
    :param nombre: Nombre del usuario.
    """
    def __init__(self, id_usuario: int, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Habitacion:
    """
    Clase que representa una habitación de hotel.

    :param numero: Número de la habitación.
    """
    def __init__(self, numero: int):
        self.numero = numero
        self.libre = True
        self.usuario = None
        self.fecha_reserva = None  # Añadimos la fecha de reserva

    def reservar(self, usuario: Usuario, fecha: str):
        """
        Reserva la habitación para un usuario en una fecha específica.

        :param usuario: Usuario que reserva la habitación.
        :param fecha: Fecha de la reserva.
        :raises ReservaException: Si la habitación ya está reservada.
        """
        if not self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está reservada.")
        
        self.libre = False
        self.usuario = usuario
        self.fecha_reserva = fecha  # Guardamos la fecha de reserva

    def liberar(self):
        """
        Libera la habitación.

        :raises ReservaException: Si la habitación ya está libre.
        """
        if self.libre:
            raise ReservaException(f"La habitación {self.numero} ya está libre.")
        self.libre = True
        self.usuario = None
        self.fecha_reserva = None

    def __str__(self):
        estado = 'Libre' if self.libre else f'Ocupada por {self.usuario}'
        return f"Habitación {self.numero} - {estado}"

class Establecimiento:
    """
    Clase base para representar un establecimiento.

    :param id_establecimiento: ID único del establecimiento.
    :param nombre: Nombre del establecimiento.
    :param direccion: Dirección del establecimiento.
    """
    def __init__(self, id_establecimiento: int, nombre: str, direccion: str):
        self.id_establecimiento = id_establecimiento
        self.nombre = nombre
        self.direccion = direccion
    
    def mostrar_informacion(self):
        """
        Muestra la información del establecimiento.
        """
        print(f"Nombre: {self.nombre}")
        print(f"Dirección: {self.direccion}")

# Clase Hotel heredada de Establecimiento
class Hotel(Establecimiento):
    """
    Clase que representa un hotel.

    :param id_establecimiento: ID único del hotel.
    :param nombre: Nombre del hotel.
    :param direccion: Dirección del hotel.
    :param categoria: Categoría del hotel (estrellas).
    :param num_habitaciones: Número de habitaciones del hotel.
    """
    def __init__(self, id_establecimiento: int, nombre: str, direccion: str, categoria: int, num_habitaciones: int):
        super().__init__(id_establecimiento, nombre, direccion)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i) for i in range(1, num_habitaciones + 1)]
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
            habitaciones_libres[i].reservar(usuario, "Fecha no especificada")
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

# Clase Hostal heredada de Establecimiento
class Hostal(Establecimiento):
    """
    Clase que representa un hostal.
    """
    def __init__(self, id_establecimiento: int, nombre: str, direccion: str, categoria: int, num_habitaciones: int):
        super().__init__(id_establecimiento, nombre, direccion)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i) for i in range(1, num_habitaciones + 1)]
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
            habitaciones_libres[i].reservar(usuario, "Fecha no especificada")
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

# Clase Apartamento heredada de Establecimiento
class Apartamento(Establecimiento):
    """
    Clase que representa un apartamento.
    """
    def __init__(self, id_establecimiento: int, nombre: str, direccion: str, categoria: int, num_habitaciones: int):
        super().__init__(id_establecimiento, nombre, direccion)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i) for i in range(1, num_habitaciones + 1)]
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
            habitaciones_libres[i].reservar(usuario, "Fecha no especificada")
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

# Clase Camping heredada de Establecimiento
class Camping(Establecimiento):
    """
    Clase que representa un camping.
    """
    def __init__(self, id_establecimiento: int, nombre: str, direccion: str, categoria: int, num_habitaciones: int):
        super().__init__(id_establecimiento, nombre, direccion)
        self.categoria = categoria
        self.habitaciones: List[Habitacion] = [Habitacion(i) for i in range(1, num_habitaciones + 1)]
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
            habitaciones_libres[i].reservar(usuario, "Fecha no especificada")
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

class SistemaHoteles:
    """
    Sistema de gestión de hoteles y otros establecimientos.
    """
    def __init__(self):
        self.establecimientos: Dict[int, Establecimiento] = {}  # Guardamos los establecimientos por id
        self.usuarios: Dict[int, Usuario] = {}  # Guardamos los usuarios por id

    def agregar_establecimiento(self, establecimiento: Establecimiento):
        """
        Agrega un establecimiento al sistema.

        :param establecimiento: Establecimiento a agregar.
        """
        self.establecimientos[establecimiento.id_establecimiento] = establecimiento  # Asignamos el establecimiento a un id
        print(f"Establecimiento {establecimiento.nombre} agregado al sistema.")

    def agregar_usuario(self, usuario: Usuario):
        """
        Agrega un usuario al sistema.
        """
        self.usuarios[usuario.id_usuario] = usuario
        print(f"Usuario {usuario.nombre} agregado al sistema con ID {usuario.id_usuario}.")

    def mostrar_establecimientos(self):
        """
        Muestra la información de todos los establecimientos en el sistema.
        """
        for establecimiento in self.establecimientos.values():
            establecimiento.mostrar_informacion()


# Ejemplo de uso
if __name__ == "__main__":
    sistema = SistemaHoteles()

    # Crear los establecimientos
    hotel = Hotel(1, "Hotel Playa", "Calle del Mar 789", 4, 75)
    hostal = Hostal(2, "Hostal Sol", "Calle Sol 123", 3, 20)
    apartamento = Apartamento(3, "Apartamento Luna", "Avenida Luna 456", 5, 50)
    camping = Camping(4, "Camping Estrella", "Carretera Estrella 789", 2, 100)

    # Agregar establecimientos al sistema
    sistema.agregar_establecimiento(hotel)
    sistema.agregar_establecimiento(hostal)
    sistema.agregar_establecimiento(apartamento)
    sistema.agregar_establecimiento(camping)

    # Crear los usuarios
    usuario1 = Usuario(1, "Juan Perez")
    usuario2 = Usuario(2, "Ana Gomez")
    usuario3 = Usuario(3, "Carlos Lopez")
    usuario4 = Usuario(4, "Lucia Martinez")
    usuario5 = Usuario(5, "Pedro Sanchez")

    # Agregar usuarios al sistema
    sistema.agregar_usuario(usuario1)
    sistema.agregar_usuario(usuario2)
    sistema.agregar_usuario(usuario3)
    sistema.agregar_usuario(usuario4)
    sistema.agregar_usuario(usuario5)

    # Realizar reservas en los diferentes establecimientos
    hotel.reservar_habitacion(usuario1, 2)  # Reservar 2 habitaciones en el hotel
    hostal.reservar_habitacion(usuario2, 1)  # Reservar 1 habitación en el hostal
    apartamento.reservar_habitacion(usuario3, 3)  # Reservar 3 habitaciones en el apartamento
    camping.reservar_habitacion(usuario4, 1)  # Reservar 1 habitación en el camping
    camping.reservar_habitacion(usuario5, 2)  # Reservar 2 habitaciones en el camping

    # Mostrar la información de los establecimientos después de las reservas
    print("\nInformación actualizada de los establecimientos:")
    sistema.mostrar_establecimientos()