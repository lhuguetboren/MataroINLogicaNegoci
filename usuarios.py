import json

class Cliente:
    def __init__(self, id, nombre, correo, telefono, direccion, usuario, password):
        self.id_cliente = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.usuario = usuario
        self.password = password

class Proveedor:
    def __init__(self, id, tipo, nombre, password, primeraConexion=None, ultimaConexion=None):
        self.id_proveedor = id
        self.tipo = tipo
        self.nombre = nombre
        self.password = password
        self.primeraConexion = primeraConexion
        self.ultimaConexion = ultimaConexion

class BaseDatos:
    def __init__(self, archivo_clientes, archivo_proveedores):
        self.archivo_clientes = archivo_clientes
        self.archivo_proveedores = archivo_proveedores
        self.clientes = self.cargar_datos(archivo_clientes, 'cliente')
        self.proveedores = self.cargar_datos(archivo_proveedores, 'hotel')

    def cargar_datos(self, archivo, tipo):
        with open(archivo, 'r') as f:
            data = json.load(f)
            if tipo == 'cliente':
                return {cliente['id']: Cliente(**cliente) for cliente in data['cliente']}
            elif tipo == 'hotel':
                return {proveedor['id']: Proveedor(**proveedor) for proveedor in data['hotel']}

    def guardar_datos(self):
        clientes_data = {'cliente': [vars(cliente) for cliente in self.clientes.values()]}
        proveedores_data = {'hotel': [vars(proveedor) for proveedor in self.proveedores.values()]}
        with open(self.archivo_clientes, 'w') as f:
            json.dump(clientes_data, f, indent=4)
        with open(self.archivo_proveedores, 'w') as f:
            json.dump(proveedores_data, f, indent=4)

    def agregar_cliente(self, cliente):
        self.clientes[cliente.id_cliente] = cliente
        self.guardar_datos()

    def eliminar_cliente(self, id_cliente):
        if id_cliente in self.clientes:
            del self.clientes[id_cliente]
            self.guardar_datos()

    def modificar_cliente(self, id_cliente, nuevo_cliente):
        if id_cliente in self.clientes:
            self.clientes[id_cliente] = nuevo_cliente
            self.guardar_datos()

    def agregar_proveedor(self, proveedor):
        self.proveedores[proveedor.id_proveedor] = proveedor
        self.guardar_datos()

    def eliminar_proveedor(self, id_proveedor):
        if id_proveedor in self.proveedores:
            del self.proveedores[id_proveedor]
            self.guardar_datos()

    def modificar_proveedor(self, id_proveedor, nuevo_proveedor):
        if id_proveedor in self.proveedores:
            self.proveedores[id_proveedor] = nuevo_proveedor
            self.guardar_datos()

# Cargar la base de datos desde archivos JSON
archivo_clientes = "MataroIN/servidor/clientes.json"
archivo_proveedores = "MataroIN/servidor/proveedores.json"
base_datos = BaseDatos(archivo_clientes, archivo_proveedores)

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
    print(vars(proveedor))
