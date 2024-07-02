import diccionarioArchivo
from datos import alojamientos,clientes,proveedores,blogs,feeds,idiomas,municipios,transportes
 

class cargarDiccionario:
    def __init__(self, datos):
        self.datos = datos

    def listar_elementos(self):
        for lista in self.datos.items():
            for elemento in lista:
                if(type(elemento) is list):
                    for registro in elemento:
                        print(registro["id"])
                        print(registro["nombre"])

    def agregar_elemento(self, tipo, nuevo_elemento):
        if tipo in self.datos:
            self.datos[tipo].append(nuevo_elemento)
        else:
            self.datos[tipo] = [nuevo_elemento]

    def crear_clave_principal(self):
        nueva_clave = 'alojamientos_generales'
        self.datos[nueva_clave] = []
        
        for tipo, lista in self.datos.items():
            if tipo != nueva_clave:
                for elemento in lista:
                    nuevo_elemento = {
                        'tipo': tipo[:-1].capitalize(),
                        'nombre': elemento['nombre'],
                        'precio': elemento.get('precio'),
                        'habitaciones-disponibles': elemento.get('habitaciones-disponibles'),
                        'poblacion': elemento['poblacion'],
                        'direccion': elemento['direccion'],
                        'telefono': elemento['telefono'],
                        'correo': elemento['correo'],
                        'imagen': elemento['imagen'],
                        'servicios': elemento['servicios'],
                        'fechas': elemento['fechas'],
                        'fechaxhabitaciones': elemento['fechaxhabitaciones'],
                        'descripcion': elemento['descripcion'],
                    }
                    self.datos[nueva_clave].append(nuevo_elemento)

aloj = cargarDiccionario(alojamientos)

aloj2 = cargarDiccionario(aloj)


# Ejemplo de uso
transporte = cargarDiccionario(transportes)
transporte.listar_elementos()



cliente = cargarDiccionario(clientes)
cliente.listar_elementos()

proveedor = cargarDiccionario(proveedores)
proveedor.listar_elementos()

blog = cargarDiccionario(blogs)
blog.listar_elementos()

feed = cargarDiccionario(feeds)
feed.listar_elementos()

idioma = cargarDiccionario(idiomas)
idioma.listar_elementos()

municipio = cargarDiccionario(municipios)
municipio.listar_elementos()

transporte = cargarDiccionario(transportes)
transporte.listar_elementos()

