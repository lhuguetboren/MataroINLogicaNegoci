from sqlalchemy import create_engine, Column, Integer, Float,String,DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import pydoc

# Configuración de la conexión a la base de datos
engine = create_engine("mysql://flask:flask2024@localhost/mataroin",echo=True)

# Declarative base
Base = declarative_base()

class Destino(Base):
    __tablename__ = 'destino'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_localidad = Column(Integer, ForeignKey('localidades.id'), nullable=True)
    id_alojamiento = Column(Integer, ForeignKey('alojamientos.id'), nullable=True)
    temporada_verano = Column(Float, nullable=True)
    temporada_primavera = Column(Float, nullable=True)
    temporada_especial = Column(Float, nullable=True)
    tarjeta_oro = Column(Float, nullable=True)
    tarjeta_plata = Column(Float, nullable=True)
    dextras_verano = Column(Float, nullable=True)
    dextras_primavera = Column(Float, nullable=True)
    dextras_resto = Column(Float, nullable=True)
    f_crea = Column(DateTime, nullable=True)
    f_mod = Column(DateTime, nullable=True)
    f_elim = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<alojamientos(id='{self.id}', idlocalidiad={self.id_localidad} id:alojamiento{self.id_alojamiento})>"




from datetime import datetime
 
def calcular_valor_promedio(info):
    # Obtener la fecha actual
    fecha_actual = datetime.now()
 
    # Valores proporcionados
    temporada = info["temporada"]
    tarjetas = info["tarjetas"]
    dextras = info["dextras"]
    usabilidad = float(info["usabilidad"])  # Convertir a float si es necesario
 
    # Definir los ponderadores por defecto y ajustar según la temporada actual
    ponderadores = {
        "temporada": 1.0,
        "tarjetas": 1.0,
        "dextras": 1.0,
        "usabilidad": 1.0
    }
 
    # Evaluar temporada actual y ajustar ponderadores
    if fecha_actual.month in [6, 7, 8]:  # Verano (junio, julio, agosto)
        ponderadores["temporada"] *= temporada.get("verano", 6.0)
        ponderadores["dextras"] *= dextras.get("verano", 1.0)
    elif fecha_actual.month in [3, 4, 5]:  # Primavera (marzo, abril, mayo)
        ponderadores["temporada"] *= temporada.get("primavera", 4.0)
        ponderadores["dextras"] *= dextras.get("primavera", 3.0)
    else:  # Resto del año
        ponderadores["temporada"] *= temporada.get("especial", 2.0)
        ponderadores["dextras"] *= dextras.get("resto", 5.0)
 
    # Aplicar ponderadores para tarjetas
    ponderadores["tarjetas"] *= float(tarjetas.get("oro", 4))  # 0 si no hay "oro"
    ponderadores["tarjetas"] += float(tarjetas.get("plata", 2))  # Sumar "plata" si existe
 
    # Calcular el valor promedio
    valor_promedio = (ponderadores["temporada"] + ponderadores["tarjetas"] + ponderadores["dextras"]) * usabilidad / 5.0
 
    return valor_promedio
 

 


# Creación de las tablas
Base.metadata.create_all(engine)

# Creación de la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Consulta para verificar la inserción
aloj = session.query(Destino).all()
for al in aloj:
   # Ejemplo de uso con los datos proporcionados
    info = {
        "id_alojamiento": al.id_alojamiento,
        "id_localidad": al.id_localidad,
        "temporada": {"especial": al.temporada_especial, "verano": al.temporada_verano, "primavera": al.temporada_primavera},
        "tarjetas": {"oro": al.tarjeta_oro, "plata": al.tarjeta_plata},
        "dextras": {"verano": al.dextras_verano, "primavera": al.dextras_primavera, "resto": al.dextras_resto},
        "usabilidad": "5"
    }

    valor = calcular_valor_promedio(info)
    print(f"El valor promedio calculado es: {valor}")

