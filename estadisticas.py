import logging
import pandas as pd
import json
from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String,DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased
from datetime import datetime
from basededatos import result_list


app = Flask(__name__)
#log_df = pd.read_json('log.json') // Esto espa leer Json

#Pones el diccionario 
log_df = pd.DataFrame(result_list)

# Configuración de la conexión a la base de datos
engine = create_engine("mysql://flask:flask2024@localhost/mataroin", echo=False)
# Declarative base
Base = declarative_base()

print(log_df)



@app.route('/editar')
def editar():
    # Group logs by log level and time to count the number of logs  
    grouped_logs = log_df.groupby(['Pais', 'Tag', 'Compra']).size().unstack(fill_value=0) 
    '''print("\nNumber of logs grouped by level and time：")  
    print(grouped_logs)'''

    json_result = grouped_logs.to_json(orient='index')
    #print(json_result)

    with open("templates/estadisticas.json", 'w') as f:
        f.write(json_result)
    
    return "Ok"


'''Mostras Json en html'''
@app.route('/visualizar')
def visualizar():
    # Cargar la cadena JSON como un diccionario
    with open("templates/estadisticas.json", 'r', encoding='utf-8') as archivo:
        datajson = json.load(archivo)

    # Convertir el JSON a DataFrame
    df = pd.DataFrame.from_dict(datajson, orient='index')
    df.index = pd.MultiIndex.from_tuples([eval(i) for i in df.index], names=["Pais", "Ciudad"])
    df = df.reset_index()

    # Ordenar la tabla según sea necesario
    df = df.sort_values(by=["Pais", "Ciudad"])

    # Convertir el DataFrame a HTML
    table_html = df.to_html(index=False)
    return render_template('index.html', table_html=table_html)

def main():     
    app.run(debug=True, host='0.0.0.0', port=5000)

#Arranca 
if __name__ == '__main__':
    main()