import json
import pydoc

class Cliente:
    """
    Clase que representa un cliente.

    :param id: ID del cliente.
    :param nombre: Nombre del cliente.
    :param correo: Correo electrónico del cliente.
    :param telefono: Teléfono del cliente.
    :param direccion: Dirección del cliente.
    :param usuario: Nombre de usuario del cliente.
    :param password: Contraseña del cliente.
    """
    def __init__(self, id, nombre, correo, telefono, direccion, usuario, password):
        self.id_cliente = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.usuario = usuario
        self.password = password

class Proveedor:
    """
    Clase que representa un proveedor.

    :param id: ID del proveedor.
    :param tipo: Tipo de proveedor.
    :param nombre: Nombre del proveedor.
    :param password: Contraseña del proveedor.
    :param primeraConexion: Fecha de la primera conexión del proveedor.
    :param ultimaConexion: Fecha de la última conexión del proveedor.
    """
    def __init__(self, id, tipo, nombre, password, primeraConexion=None, ultimaConexion=None):
        self.id_proveedor = id
        self.tipo = tipo
        self.nombre = nombre
        self.password = password
        self.primeraConexion = primeraConexion
        self.ultimaConexion = ultimaConexion

class BaseDatos:
    """
    Clase que representa la base de datos para clientes y proveedores.

    :param archivo_clientes: Ruta del archivo JSON que contiene los datos de los clientes.
    :param archivo_proveedores: Ruta del archivo JSON que contiene los datos de los proveedores.
    """
    def __init__(self, archivo_clientes, archivo_proveedores):
        self.archivo_clientes = archivo_clientes
        self.archivo_proveedores = archivo_proveedores
        self.clientes = self.cargar_datos(archivo_clientes, 'cliente')
        self.proveedores = self.cargar_datos(archivo_proveedores, 'hotel')

    def cargar_datos(self, archivo, tipo):
        """
        Carga los datos desde un archivo JSON.

        :param archivo: Ruta del archivo JSON.
        :param tipo: Tipo de datos a cargar ('cliente' o 'hotel').
        :return: Diccionario con los datos cargados.
        """
        with open(archivo, 'r') as f:
            data = json.load(f)
            if tipo == 'cliente':
                return {cliente['id_cliente']: Cliente(**cliente) for cliente in data['cliente']}
            elif tipo == 'hotel':
                return {proveedor['id_proveedor']: Proveedor(**proveedor) for proveedor in data['hotel']}

    def guardar_datos(self):
        """
        Guarda los datos de clientes y proveedores en archivos JSON.
        """
        clientes_data = {'cliente': [vars(cliente) for cliente in self.clientes.values()]}
        proveedores_data = {'hotel': [vars(proveedor) for proveedor in self.proveedores.values()]}
        with open(self.archivo_clientes, 'w') as f:
            json.dump(clientes_data, f, indent=4)
        with open(self.archivo_proveedores, 'w') as f:
            json.dump(proveedores_data, f, indent=4)

    def agregar_cliente(self, cliente):
        """
        Agrega un cliente a la base de datos y guarda los cambios.

        :param cliente: Instancia de Cliente a agregar.
        """
        self.clientes[cliente.id_cliente] = cliente
        self.guardar_datos()

    def eliminar_cliente(self, id_cliente):
        """
        Elimina un cliente de la base de datos y guarda los cambios.

        :param id_cliente: ID del cliente a eliminar.
        """
        if id_cliente in self.clientes:
            del self.clientes[id_cliente]
            self.guardar_datos()

    def modificar_cliente(self, id_cliente, nuevo_cliente):
        """
        Modifica los datos de un cliente en la base de datos y guarda los cambios.

        :param id_cliente: ID del cliente a modificar.
        :param nuevo_cliente: Instancia de Cliente con los nuevos datos.
        """
        if id_cliente in self.clientes:
            self.clientes[id_cliente] = nuevo_cliente
            self.guardar_datos()

    def agregar_proveedor(self, proveedor):
        """
        Agrega un proveedor a la base de datos y guarda los cambios.

        :param proveedor: Instancia de Proveedor a agregar.
        """
        self.proveedores[proveedor.id_proveedor] = proveedor
        self.guardar_datos()

    def eliminar_proveedor(self, id_proveedor):
        """
        Elimina un proveedor de la base de datos y guarda los cambios.

        :param id_proveedor: ID del proveedor a eliminar.
        """
        if id_proveedor in self.proveedores:
            del self.proveedores[id_proveedor]
            self.guardar_datos()

    def modificar_proveedor(self, id_proveedor, nuevo_proveedor):
        """
        Modifica los datos de un proveedor en la base de datos y guarda los cambios.

        :param id_proveedor: ID del proveedor a modificar.
        :param nuevo_proveedor: Instancia de Proveedor con los nuevos datos.
        """
        if id_proveedor in self.proveedores:
            self.proveedores[id_proveedor] = nuevo_proveedor
            self.guardar_datos()

# Cambiar la carga a la base de datos en lugar de''' archivos JSON
'''
#archivo_clientes = "static/json/clientes.json"
#archivo_proveedores = "static/json/proveedores.json"
base_datos = BaseDatos("", "")

# Ejemplo de cómo modificar un cliente
nuevo_cliente = Cliente(2, 'Karl Denmark Jr.', '', '', '', 'Karl', 'Denmark')
base_datos.modificar_cliente(2, nuevo_cliente)

# Ejemplo de cómo eliminar un proveedor
base_datos.eliminar_proveedor(1)

# Mostrar los clientes y proveedores actuales
print("Clientes:")
for cliente in base_datos.clientes.values():
    print(vars(cliente))

print("\nProveedores:")
for proveedor in base_datos.proveedores.values():
    print(vars(proveedor))'''
