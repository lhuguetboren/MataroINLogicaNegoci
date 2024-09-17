import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from models import Alojamientos, AlojamientosFechas, AlojamientosServicios, Servicios, Hoteles, session,engine

# Creación de la sesión
Session = sessionmaker(bind=engine)
session = Session()

def obtener_datos_hotel(nombre_hotel):
    query = """
    SELECT a.*, b.*, c.*, c1.*, d.* 
    FROM alojamientos a
    LEFT JOIN alojamientos_fechas b ON b.id_alojamiento = a.id
    LEFT JOIN alojamientos_servicios c ON c.id_alojamientos = a.id
    LEFT JOIN servicios c1 ON c1.id = c.id_servicios
    LEFT JOIN hoteles d ON d.id = a.id AND a.tipo = 'hotel'
    WHERE a.tipo = 'hotel' AND a.nombre = :nombre_hotel
    """
    
    result = session.execute(text(query), {'nombre_hotel': nombre_hotel}).fetchall()

    # Convertimos el resultado en un diccionario
    data = [dict(row._mapping) for row in result]
    # Convertimos el diccionario a JSON
    json_data = json.dumps(data, default=str)
    
    return json_data




# Creación de la sesión (si no está creada ya en el modelo)
Session = sessionmaker(bind=engine)
session = Session()

def obtener_datos_hotel2(nombre_hotel):
    # Realizamos la consulta usando SQLAlchemy ORM
    result = (
        session.query(Alojamientos, AlojamientosFechas, AlojamientosServicios, Servicios, Hoteles)
        .join(AlojamientosFechas, AlojamientosFechas.id_alojamiento == Alojamientos.id, isouter=True)
        .join(AlojamientosServicios, AlojamientosServicios.id_alojamientos == Alojamientos.id, isouter=True)
        .join(Servicios, Servicios.id == AlojamientosServicios.id_servicios, isouter=True)
        .join(Hoteles, Hoteles.id == Alojamientos.id, isouter=True)
        .filter(Alojamientos.tipo == 'hotel', Alojamientos.nombre == nombre_hotel)
        .all()
    )

    # Convertimos el resultado en un diccionario
    data = []
    for alojamiento, fecha, servicio_alojamiento, servicio, hotel in result:
        data.append({
            "alojamiento": {
                "id": alojamiento.id,
                "nombre": alojamiento.nombre,
                "tipo": alojamiento.tipo,
            },
            "servicio": {
                "id": servicio.id if servicio else None,
                "nombre": servicio.nombre if servicio else None
            },
            "hotel": {
                "id": hotel.id if hotel else None,
                "nombre": alojamiento.nombre if hotel else None
            }
        })

    # Convertimos el diccionario a JSON
    json_data = json.dumps(data, default=str)
    
    return json_data


print(obtener_datos_hotel('Hotel Barcelona'))
print('############3')
print(obtener_datos_hotel2('Hotel Barcelona'))