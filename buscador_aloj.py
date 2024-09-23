import pydoc
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased
from decimal import Decimal

from models import  Alojamientos, AlojamientosFechas, Localidades, Hoteles, Apartamentos, Campings, Servicios, Hostales, AlojamientosServicios, FechasAlojamientos, get_db_session
from datetime import datetime, date


def buscar_alojamiento_por_criterios(criterios_busqueda):
    """
    Busca alojamientos en la base de datos según los criterios de búsqueda especificados.

    :param criterios_busqueda: Lista de diccionarios con los criterios de búsqueda.
    :return: Lista de diccionarios con los alojamientos que cumplen los criterios de búsqueda.
    """
    # Construir la consulta base
    session = get_db_session()

    query = session.query(
        Alojamientos.id,Alojamientos.tipo,
        Alojamientos.nombre,
        Localidades.nombre.label('localidad_nombre'),
        Hoteles.habitaciones.label('hotel_habitaciones'),
        Hoteles.estrellas.label('hotel_estrellas'),
        Apartamentos.habitaciones.label('apartamento_habitaciones'),
        Campings.tipo_camping.label('camping_tipo_camping'),
        FechasAlojamientos.fecha.label('fecha'),
        FechasAlojamientos.precio.label('precio'),
        FechasAlojamientos.disponible.label('disponible'),
        FechasAlojamientos.libres.label('libres'),
        Servicios.nombre.label('descripcion')
    ).outerjoin(Localidades, Alojamientos.id_localidad == Localidades.id
    ).outerjoin(Hoteles, Alojamientos.id == Hoteles.id
    ).outerjoin(Apartamentos, Alojamientos.id == Apartamentos.id
    ).outerjoin(Hostales, Alojamientos.id == Hostales.id
    ).outerjoin(Campings, Alojamientos.id == Campings.id
    ).outerjoin(FechasAlojamientos, Alojamientos.id == FechasAlojamientos.id_alojamiento
    ).outerjoin(AlojamientosServicios, Alojamientos.id == AlojamientosServicios.id_alojamientos
    ).outerjoin(Servicios, AlojamientosServicios.id_servicios == Servicios.id)
    
    # Ejecutar la consulta
    resultados = query.all()
    resultados_dict = [row._asdict() for row in resultados]

    # Filtrar los resultados según los criterios de búsqueda
    resultados_filtrados = filtrar_por_criterios(resultados_dict, criterios_busqueda)

    # Cerrar la sesión
    session.close()

    return resultados_filtrados


def filtrar_por_criterios(lista, criterios):
    """
    Filtra una lista de alojamientos según los criterios especificados.

    :param lista: Lista de diccionarios con los alojamientos.
    :param criterios: Lista de diccionarios con los criterios de búsqueda.
    :return: Lista de diccionarios con los alojamientos que cumplen los criterios.
    """
    # Precios por defecto
    precio_min = Decimal("0.00")
    precio_max = Decimal("999999.99")
    fecha_entrada = None
    fecha_salida = None

    # Extraemos los valores de precio y fechas de los criterios
    for criterio in criterios:
        if 'fecha_entrada' in criterio:  
            fecha_entrada = datetime.strptime(criterio['fecha_entrada'], '%Y-%m-%d').date()
        if 'fecha_salida' in criterio:
            fecha_salida = datetime.strptime(criterio['fecha_salida'], '%Y-%m-%d').date()
        if 'precio_min' in criterio:
            precio_min = criterio['precio_min']
        if 'precio_max' in criterio:
            precio_max = criterio['precio_max']

    def cumple_criterios(elemento):
        """
        Verifica si un alojamiento cumple con los criterios de búsqueda.

        :param elemento: Diccionario con los datos del alojamiento.
        :return: True si el alojamiento cumple con los criterios, False en caso contrario.
        """
        # Comprobamos el precio
        if elemento['precio'] is not None:
            if elemento['precio'] < precio_min or elemento['precio'] > precio_max:
                return False
        # Comprobamos las fechas
        if fecha_entrada and fecha_salida and elemento['fecha'] is not None:
            fecha_registro = elemento['fecha']
            if fecha_registro < fecha_entrada or fecha_registro > fecha_salida: 
                return False

        # Comprobamos otros criterios
        for criterio in criterios:
            for campo, valor in criterio.items():
                if campo != 'precio_min' and campo != 'precio_max' and campo != 'fecha_entrada' and campo != 'fecha_salida':
                    if campo in elemento and elemento[campo] != valor:
                        return False
        return True

    return [elemento for elemento in lista if cumple_criterios(elemento)]


def decimal_default(obj):
    """
    Convierte objetos Decimal y date a tipos compatibles con JSON.

    :param obj: Objeto a convertir
    :return: Objeto convertido
    :raises TypeError: Si el objeto no es serializable.
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
