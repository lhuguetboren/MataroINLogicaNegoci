import json
import diccionarioArchivo

combined_dataT = {}
municipio = diccionarioArchivo.recuperar_diccionario("MataroIN/servidor/municipios.json")
alojamiento = diccionarioArchivo.recuperar_diccionario("MataroIN/servidor/alojamientos.json")



def combine_data(municipios_data, alojamientos_data):
    combined_data = {}
    for alojamiento in alojamientos_data:
        poblacion = alojamiento['poblacion']
        for k in municipios_data:
            if poblacion==k["nombre"]:
                municipio_info = municipios_data[k["id"]-1]
                alojamiento['ponderacion'] = {
                    'fiestas_patronales': municipio_info['fiestasPatronales'],
                    'conciertos': municipio_info['conciertos'],
                    'playas': municipio_info['playas'],
                    'zona_turistica': municipio_info['zonaTuristica'],
                    'gastronomia': municipio_info['gastronomia']
                }
                combined_data[alojamiento['nombre']] = alojamiento
    return combined_data


# Archivo JSON de salida

combined_dataT.update(combine_data(municipio['municipio'], alojamiento['hoteles']))
combined_dataT.update(combine_data(municipio['municipio'], alojamiento['hostales']))

# Combinar los datos
diccionarioArchivo.guardar_diccionario(combined_dataT,"MataroIn/servidor/plususabilidad.json")



