from datetime import date
import diccionarioArchivo
class Cliente:
    def __init__(self, nombre, categoria_fidelizacion):
        self.nombre = nombre
        self.categoria_fidelizacion = categoria_fidelizacion
 
    def obtener_descuento(self):
        if self.categoria_fidelizacion == 'Oro':
            return 0.20
        elif self.categoria_fidelizacion == 'Plata':
            return 0.10
        else:
            return 0.00
 
class Alojamiento:
    def __init__(self, nombre, propietario, tarifa, destino):
        self.nombre = nombre
        self.propietario = propietario
        self.tarifa = tarifa
        self.destino = destino
 
    def calcular_precio_final(self, cliente, fecha_reserva):
        precio_base = self.tarifa
        descuentos = [cliente.obtener_descuento()]
       
        # Añadir aportes del ayuntamiento basados en la temporada y eventos especiales
        descuentos.append(self.destino.obtener_aporte_temporada(fecha_reserva))
        descuentos.append(self.destino.obtener_aporte_evento(fecha_reserva))
       
        # Aplicar descuentos secuencialmente
        precio_final = precio_base
        for descuento in descuentos:
            precio_final *= (1 - descuento)
       
        return precio_final
 
class Destino:
    def __init__(self, nombre):
        self.nombre = nombre
        self.aportes_temporada = {}
        self.eventos_especiales = {}
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "aportes_temporada": self.aportes_temporada,
            "eventos_especiales": self.eventos_especiales
        }
    def definir_aporte_temporada(self, temporada, porcentaje_aporte):
        self.aportes_temporada[temporada] = porcentaje_aporte


    def definir_evento_especial(self, fecha, porcentaje_aporte):
        self.eventos_especiales[fecha] = porcentaje_aporte
 
    def obtener_aporte_temporada(self, fecha):
        # Suponiendo temporadas definidas como tuplas de fechas (inicio, fin)
        for temporada, aporte in self.aportes_temporada.items():
            if aporte[1] <= fecha <= aporte[2]:
                return aporte[0]
        return 0
 
    def obtener_aporte_evento(self, fecha):
        return self.eventos_especiales.get(fecha, 0)
 
# Ejemplo de uso
 
# Definición del destino con aportes según la temporada y eventos especiales
destino1 = Destino("Madrid")
destino1.definir_aporte_temporada("primavera", [0.05,20240401,20240801])  # Temporada baja
destino1.definir_aporte_temporada("verano", [0.10,20240401,20240801])  # Temporada alta
destino1.definir_evento_especial(20240505, 0.15)  # Navidad
diccionarioArchivo.guardar_diccionario(destino1.to_dict(),"destinos.json")
 
# Definición del alojamiento en el destino
alojamiento1 = Alojamiento("Hotel Central", "Maria", 100, destino1)
 
# Definición del cliente
cliente1 = Cliente("Juan", "Oro")
 
# Cálculo del precio final para una fecha específica
fecha_reserva = 20240501
precio_final = alojamiento1.calcular_precio_final(cliente1, fecha_reserva)
print(f"El precio final para {cliente1.nombre} en {alojamiento1.nombre} el {fecha_reserva} es {precio_final:.2f} euros.")
 
print(destino1.to_dict())
diccionarioArchivo.guardar_diccionario(destino1.to_dict(),"destinos.json")
# Convertir la instancia a un diccionario
