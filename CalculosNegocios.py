import pydoc
from flask import jsonify
from datetime import datetime
from models import get_db_session, Alojamientos, Localidades,Cookies, Paises, Dispositivos, Tags, UsabDatos, UsabRelacion, Destino, Usab
from sqlalchemy import desc, distinct
import numpy as np
import pandas as pd
from sqlalchemy import func

def calcular_media(valores):
    """
    Calcula la media de una lista de valores.

    :param valores: Lista de valores numéricos.
    :return: Media de los valores.
    """
    return np.mean(valores)

def calcular_mediana(valores):
    """
    Calcula la mediana de una lista de valores.

    :param valores: Lista de valores numéricos.
    :return: Mediana de los valores.
    """
    return np.median(valores)

def calcular_moda(valores):
    """
    Calcula la moda de una lista de valores.

    :param valores: Lista de valores numéricos.
    :return: Moda de los valores.
    """
    vals, counts = np.unique(valores, return_counts=True)
    return vals[counts == np.max(counts)]

def recuperaDatos():
    """
    Recupera datos de cookies, países, dispositivos y tags de la base de datos y los convierte en una lista de diccionarios.

    :return: Lista de diccionarios con los datos recuperados.
    """
    session = get_db_session()

    query = (
        session.query(Cookies, Paises, Dispositivos, Tags)
        .outerjoin(Paises, Cookies.id_pais == Paises.id)
        .outerjoin(Dispositivos, Cookies.id_dispositivo == Dispositivos.id)
        .outerjoin(Tags, Cookies.id_tag == Tags.id)
    )

    results = query.filter(Cookies.id != None)

    result_list = []

    for cook, pai, dip, tac in results:
        result_dict = {
            "Pais": pai.nombre if pai.nombre is not None else '',
            "cliente": cook.id_dispositivo,
            "Timestamp": cook.fecha_y_hora.strftime('%Y-%m-%d %H:%M:%S'),
            "Tag": tac.nombre,
            'Compra': cook.comprar
        }
        result_list.append(result_dict)
    return result_list

def calculaUsabilidad():
    """
    Calcula las estadísticas de usabilidad (media y mediana) y actualiza o crea registros en la tabla UsabDatos.

    :return: "ok" si la operación se realiza correctamente.
    """
    session = get_db_session()

    ids_usab = session.query(
        UsabRelacion.id_alojamientos,
        UsabRelacion.id_usab,
        func.group_concat(UsabRelacion.valor)
    ).group_by(
        UsabRelacion.id_alojamientos,
        UsabRelacion.id_usab
    ).all()

    for alojt, ust, valort in ids_usab:
        v = [int(x) for x in valort.split(',')]
        media = float(calcular_media(v))
        mediana = float(calcular_mediana(v))

        usab_datos_entry = session.query(UsabDatos).filter_by(id_usab=ust,id_alojamientos=alojt).first()
        
        if usab_datos_entry:
            usab_datos_entry.media = media
            usab_datos_entry.mediana = mediana
        else:
            nuevo_usab_datos = UsabDatos(
                id_alojamientos=alojt,
                id_usab=ust,
                media=media,
                mediana=mediana,
                moda=0
            )
            session.add(nuevo_usab_datos)

        session.commit()
    return "ok"

def calcular_valor_promedio_destinos(info):
    """
    Calcula el valor promedio de los destinos según la información proporcionada.

    :param info: Diccionario con la información de los destinos.
    :return: Valor promedio calculado.
    """
    session = get_db_session()

    fecha_actual = datetime.now()
    temporada = info["temporada"]
    tarjetas = info["tarjetas"]
    dextras = info["dextras"]
    usabilidad = float(info["usabilidad"])

    ponderadores = {
        "temporada": 1.0,
        "tarjetas": 1.0,
        "dextras": 1.0,
        "usabilidad": 1.0
    }

    if fecha_actual.month in [6, 7, 8]:
        a = 1
    elif fecha_actual.month in [3, 4, 5]:

        ponderadores["temporada"] *= temporada.get("primavera", 4.0) if temporada.get("primavera", 4.0) is not None else 0
        ponderadores["dextras"] *= dextras.get("primavera", 3.0) if dextras.get("primavera", 3.0) is not None else 0


        
    else:
        ponderadores["temporada"] *= temporada.get("especial", 2.0) if temporada.get("especial", 2.0) is not None else 0
        ponderadores["dextras"] *= dextras.get("resto", 2.0) if dextras.get("resto", 2.0) is not None else 0

        


    valor_promedio = 0
    try:
        valor_promedio = (ponderadores["temporada"] + ponderadores["tarjetas"] + ponderadores["dextras"]) * usabilidad / 5.0
        dest = session.query(Destino).filter_by(id=info["id"]).first()
        if dest:
            dest.resultado = valor_promedio
            session.commit()
        else:
            print(f'No se encuentra el ID {info["id"]}')
    finally:
        print('tarjetas')

    return valor_promedio

def devulvem3():
    """
    Devuelve los tres destinos con los mejores resultados.

    :return: Lista de diccionarios con los tres mejores destinos.
    """
    session = get_db_session()

    resultados = session.query(
    Localidades.nombre.label('nombre_localidad'),
    Alojamientos.nombre.label('nombre_alojamiento'),
    Destino.resultado.label('resultado')
).join(Alojamientos, Destino.id_alojamiento == Alojamientos.id, isouter=True)\
 .join(Localidades, Destino.id_localidad == Localidades.id, isouter=True)\
 .group_by(Localidades.nombre, Alojamientos.nombre, Destino.resultado).all()

    resultados_json = [
    {
        "nombre_localidad": resultado.nombre_localidad,
        "nombre_alojamiento": resultado.nombre_alojamiento,
        "resultado": resultado.resultado
    }
    for resultado in resultados
]

    return resultados_json


def devuelveUsabLocalidades ():
    session = get_db_session()        
    resultados = session.query(
    Usab.nombre.label('nombre_usab'),
    Localidades.nombre.label('nombre_localidad'),
    func.round(func.avg(UsabDatos.media)).label('media_promedio'),
    func.round(func.avg(UsabDatos.mediana)).label('mediana_promedio')
        ).join(Alojamientos, UsabDatos.id_alojamientos == Alojamientos.id, isouter=True)\
        .join(Localidades, Alojamientos.id_localidad == Localidades.id, isouter=True)\
        .join(Usab, UsabDatos.id_usab == Usab.id, isouter=True)\
        .group_by(Alojamientos.id_localidad, UsabDatos.id_usab).all()

    
    resultados_json = [
    {
         "nombre_usab": resultado.nombre_usab,
         "nombre_localidad": resultado.nombre_localidad,
        "media_promedio": resultado.media_promedio,
        "media_promedio": resultado.mediana_promedio,

    }
    for resultado in resultados
]

    return resultados_json


def devuelveUsabAlojamientos ():
    session = get_db_session()        
    resultados =session.query(
    Usab.nombre.label('nombre_usab'),
    Localidades.nombre.label('nombre_localidad'),
    Alojamientos.nombre.label('nombre_alojamiento'),
    func.round(func.avg(UsabDatos.media)).label('media_promedio'),
    func.round(func.avg(UsabDatos.mediana)).label('mediana_promedio')
        ).join(Alojamientos, UsabDatos.id_alojamientos == Alojamientos.id, isouter=True)\
        .join(Localidades, Alojamientos.id_localidad == Localidades.id, isouter=True)\
        .join(Usab, UsabDatos.id_usab == Usab.id, isouter=True)\
        .group_by(Alojamientos.id, Alojamientos.id_localidad, UsabDatos.id_usab).all()
    
    resultados_json = [
    {
         "nombre_usab": resultado.nombre_usab,
         "nombre_localidad": resultado.nombre_localidad,
                  "nombre_localidad": resultado.nombre_alojamiento,

        "media_promedio": resultado.media_promedio,
        "media_promedio": resultado.mediana_promedio,

    }
    for resultado in resultados
]

    return resultados_json



def calcula_destinos():
    """
    Calcula los destinos y actualiza los resultados en la base de datos.

    :return: JSON con el resultado de la operación.
    """
    session = get_db_session()

    destin = session.query(Destino).all()
    for al in destin:
        info = {
            "id": al.id,
            "id_alojamiento": al.id_alojamiento,
            "id_localidad": al.id_localidad,
            "temporada": {"especial": al.temporada_especial, "verano": al.temporada_verano, "primavera": al.temporada_primavera},
            "tarjetas": {"oro": al.tarjeta_oro, "plata": al.tarjeta_plata},
            "dextras": {"verano": al.dextras_verano, "primavera": al.dextras_primavera, "resto": al.dextras_resto},
            "usabilidad": "5"
        }

        valor = calcular_valor_promedio_destinos(info)

    return jsonify({"calculo": "ok"})

log_df = pd.DataFrame(recuperaDatos())

#print(calcula_destinos())