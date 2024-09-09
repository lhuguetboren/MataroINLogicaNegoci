# Librerías comunes
import aiohttp
import json
import os
import socket_1
from socket_1 import data_storage
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pydoc

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from securityUsers import User, users, save_users, public_key

import CalculosNegocios
from models import session, Alojamientos, Cookies, Paises#, Dispositiv
from CalculosNegocios import log_df, pd, Destino, calcula_destinos, devulvem3
from buscador_aloj import buscar_alojamiento_por_criterios

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config.from_object('config.Config')

login_manager = LoginManager(app)
login_manager.login_view = 'login'


def get_locale():
    """
    Obtiene el idioma preferido del usuario.

    :return: Idioma preferido del usuario.
    """
    return request.accept_languages.best_match(['en', 'es', 'fr'])


@login_manager.user_loader
def load_user(user_id):
    """
    Carga un usuario basado en su ID.

    :param user_id: ID del usuario
    :return: Instancia de User si el usuario existe, de lo contrario None.
    """
    user_data = users.get(user_id)
    if user_data:
        return User(id=user_id, username=user_data['username'], password=user_data['password'])
    return None

# Lista para almacenar los archivos subidos temporalmente
uploaded_files = []

app.config['UPLOAD_FOLDER'] = "./Archivos"
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # Límite de tamaño de archivo de 60 MB
app.secret_key = 'supersecretkey'

# Definición de subcarpetas para diferentes tipos de archivos
app.config['PHOTO_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], "Fotos")
app.config['VIDEO_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], "Videos")
app.config['BROCHURE_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], "Folletos")

# Crear subcarpetas si no existen
os.makedirs(app.config['PHOTO_FOLDER'], exist_ok=True)
os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
os.makedirs(app.config['BROCHURE_FOLDER'], exist_ok=True)


@app.route('/')
def negocio():
    """
    Renderiza la página principal de negocio.

    :return: Template 'admin/negocio.html'
    """
    return render_template('admin/negocio.html')


# Bloque de páginas estáticas
@app.route('/traduccion')
def traduccion():
    """
    Renderiza la página de traducción.

    :return: Template 'traduccion.html'
    """
    return render_template('traduccion.html')


@app.route('/home')
def home():
    """
    Renderiza la página principal del sitio web.

    :return: Template 'home.html'
    """
    return render_template('home.html')

@app.route('/destinos')
def destinos():
    """
    Renderiza la página de destinos.

    :return: Template 'destino.html'
    """
    return render_template('destino.html')

@app.route('/ofertas')
def ofertas():
    """
    Renderiza la página de ofertas.

    :return: Template 'ofertas.html'
    """
    return render_template('ofertas.html')

@app.route('/calendario')
def calendario():
    """
    Renderiza la página del calendario.

    :return: Template 'calendario.html'
    """
    return render_template('calendario.html')

@app.route('/loginhtml')
def loginhtml():
    """
    Renderiza la página de login.

    :return: Template 'login.html'
    """
    return render_template('login.html')

@app.route('/alojamiento/<id>')
def aloajamiento(id):
    """
    Renderiza la página de alojamiento.

    :param id: ID del alojamiento
    :return: Template 'alojamiento.html'
    """
    return render_template('alojamiento.html', id=id)

@app.route('/blog/<id>')
def blog(id):
    """
    Renderiza la página del blog.

    :param id: ID del blog
    :return: Template 'blog.html'
    """
    return render_template('blog.html', id=id)

@app.route('/videos/<id>')
def videos(id):
    """
    Renderiza la página de videos.

    :param id: ID del video
    :return: Template 'videos.html'
    """
    return render_template('videos.html', id=id)

@app.route('/folletos/<id>')
def folletos(id):
    """
    Renderiza la página de folletos.

    :param id: ID del folleto
    :return: Template 'videos.html'
    """
    return render_template('videos.html', id=id)

@app.route('/imagenes/<id>')
def imagenes(id):
    """
    Renderiza la página de imágenes.

    :param id: ID de la imagen
    :return: Template 'videos.html'
    """
    return render_template('videos.html', id=id)

@app.route('/transportes/<id>')
def transportes(id):
    """
    Renderiza la página de transportes.

    :param id: ID del transporte
    :return: Template 'transportes.html'
    """
    return render_template('transportes.html', id=id)

@app.route('/clientes/<id>')
def clientes(id):
    """
    Renderiza la página de clientes.

    :param id: ID del cliente
    :return: Template 'clientes.html'
    """
    return render_template('clientes.html', id=id)

@app.route('/proveedores/<id>')
def proveedores(id):
    """
    Renderiza la página de proveedores.

    :param id: ID del proveedor
    :return: Template 'proveedores.html'
    """
    return render_template('proveedores.html', id=id)

@app.route('/quienessomos')
def quienessomos():
    """
    Renderiza la página de "Quiénes somos".

    :return: Template 'quienessomos.html'
    """
    return render_template('quienessomos.html')

# Bloque de mantenimiento de datos

# Función para determinar la carpeta basada en el tipo de archivo
def get_folder_for_file(filename):
    """
    Determina la carpeta de destino basada en el tipo de archivo.

    :param filename: Nombre del archivo
    :return: Ruta de la carpeta correspondiente al tipo de archivo
    """
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return app.config['PHOTO_FOLDER']
    elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
        return app.config['VIDEO_FOLDER']
    elif filename.lower().endswith(('.pdf', '.doc', '.docx')):
        return app.config['BROCHURE_FOLDER']
    else:
        return app.config['UPLOAD_FOLDER']

# Bloque de login
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """
    Maneja el inicio de sesión de los usuarios.

    :return: Redirige al índice si el login es exitoso, de lo contrario renderiza el formulario de login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user_id, user_data in users.items():
            if user_data['username'] == username and user_data['password'] == password:
                user = User(id=user_id, username=username, password=user_data['password'])
                login_user(user)
                return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    """
    Maneja el cierre de sesión de los usuarios.

    :return: Redirige al formulario de login.
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/signup', methods=['GET', 'POST'])
def signup():
    """
    Maneja el registro de nuevos usuarios.

    :return: Redirige al formulario de login si el registro es exitoso, de lo contrario renderiza el formulario de registro.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user_id = str(len(users) + 1)
        users[user_id] = {'username': username, 'password': password}
        save_users(users, public_key)
        flash('User registered successfully')
        return redirect(url_for('login'))
    return render_template('admin/signup.html')

@app.route('/admin/confirmacion')
@login_required
def index():
    """
    Página principal de administración para usuarios autenticados.

    :return: Mensaje de bienvenida al usuario.
    """
    return f'Hello, {current_user.username}!'

@app.route("/admin/Biblioteca_gest")
def upload_file():
    """
    Muestra el formulario de subida de archivos y lista los archivos ya subidos.

    :return: Renderiza el template 'formulariob.html'
    """
    photos = os.listdir(app.config['PHOTO_FOLDER'])
    videos = os.listdir(app.config['VIDEO_FOLDER'])
    brochures = os.listdir(app.config['BROCHURE_FOLDER'])

    # Obtener todas las etiquetas de la base de datos
    tags = session.query(Tags).all()

    # Comprobar si se solicita mostrar la opción de eliminar un archivo
    show_delete = request.args.get('show_delete')

    delete_file_info = None
    if show_delete:
        for file in uploaded_files:
            if file['filename'] == show_delete:
                delete_file_info = file
                break

    return render_template('admin/formulariob.html', photos=photos, videos=videos, brochures=brochures, uploaded_files=uploaded_files, delete_file_info=delete_file_info, tags=tags)

# Ruta para manejar la subida de archivos
@app.route("/admin/uploader", methods=['POST'])
def uploader():
    """
    Maneja la subida de archivos.

    :return: Redirige a la ruta principal o renderiza mensajes de error
    """
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        descripcion = request.form['descripcion']
        tag_ids = request.form.getlist('tag')  # Obtener las etiquetas seleccionadas
        f = request.files['archivo']
        
        filename = secure_filename(f.filename)
        folder = get_folder_for_file(filename)
        filepath = os.path.join(folder, filename)
        file_format = filename.rsplit('.', 1)[1].lower()

        # Comprobar si el archivo ya existe
        if os.path.exists(filepath):
            flash(f"El archivo '{filename}' ya está subido. Puedes eliminarlo a continuación si lo deseas.")
            return redirect(url_for('upload_file', show_delete=filename))

        # Guardar el archivo
        f.save(filepath)

        duration = None
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
            try:
                a=1
                # Obtener la duración del video
                #video = VideoFileClip(filepath)
                #duration = video.duration
                #video.reader.close()  
                #video.audio.reader.close_proc() 
            except Exception as e:
                print(f"Error al obtener la duración del video: {e}")

        flash(f"Archivo '{filename}' subido exitosamente por {nombre} {apellidos}.")

        # Determinar el tipo de archivo
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            tipo = "foto"
        elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
            tipo = "video"
        elif filename.lower().endswith(('.pdf', '.doc', '.docx')):
            tipo = "folleto"

        # Obtener las etiquetas seleccionadas
        tags_seleccionados = [session.query(Tags).get(int(tag_id)) for tag_id in tag_ids]
        
        # Crear una nueva entrada en la base de datos
        nueva_entrada = Biblioteca(
            tipo=tipo,
            nombre=nombre,
            descripcion=descripcion,
            filename=filename,
            duracion=duration,
            formato=file_format,
            tags_relacion=[Tags(origen="biblioteca", id_tag=tag.id) for tag in tags_seleccionados]
        )

        # Guardar la nueva entrada en la base de datos
        session.add(nueva_entrada)
        session.commit()

        return redirect(url_for('upload_file'))

# Ruta para editar archivos
@app.route("/admin/edit/<folder>/<filename>", methods=['GET', 'POST'])
def edit_file(folder, filename):
    """
    Permite renombrar y actualizar la descripción de un archivo.

    :param folder: Nombre de la carpeta
    :param filename: Nombre del archivo
    :return: Renderiza el template 'edit.html' o redirige a la ruta principal
    """
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    file_entry = session.query(Biblioteca).filter_by(filename=filename).first()

    if request.method == 'POST':
        new_name = request.form['new_name']
        new_name = secure_filename(new_name)
        new_descripcion = request.form['descripcion']
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # Comprobar si el nuevo nombre de archivo ya existe
        if os.path.exists(new_path) and new_name != filename:
            flash(f"El archivo '{new_name}' ya existe en la carpeta.")
            return redirect(url_for('upload_file'))

        # Renombrar el archivo
        os.rename(old_path, new_path)
        flash(f"Archivo renombrado exitosamente a '{new_name}'.")

        # Actualizar los detalles del archivo en la base de datos
        if file_entry:
            file_entry.filename = new_name
            file_entry.descripcion = new_descripcion
            file_entry.f_mod = get_current_time_in_spain()
            session.commit()

        return redirect(url_for('upload_file'))

    return render_template('admin/editb.html', folder=folder, filename=filename, file=file_entry)

# Ruta para eliminar archivos
@app.route("/admin/delete/<folder>/<filename>", methods=['POST'])
def delete_file(folder, filename):
    """
    Maneja la eliminación de archivos.

    :param folder: Nombre de la carpeta
    :param filename: Nombre del archivo
    :return: Redirige a la ruta principal
    """
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    
    if os.path.exists(file_path):
        # Eliminar el archivo del sistema de archivos
        os.remove(file_path)
        flash(f"Archivo '{filename}' borrado exitosamente.")
        
        # Eliminar la entrada del archivo y sus relaciones en la base de datos
        file_entry = session.query(Biblioteca).filter_by(filename=filename).first()
        if file_entry:
            tags_entries = session.query(TagsRelacion).filter_by(id_origen=file_entry.id).all()
            for tag_entry in tags_entries:
                session.delete(tag_entry)

            session.delete(file_entry)
            session.commit()
    else:
        flash(f"El archivo '{filename}' no existe.")
    
    return redirect(url_for('upload_file'))

# Ruta para servir archivos subidos
@app.route('/admin/uploads/<folder>/<filename>')
def uploaded_file(folder, filename):
    """
    Permite la descarga de archivos subidos.

    :param folder: Nombre de la carpeta
    :param filename: Nombre del archivo
    :return: Envía el archivo desde el directorio de subida
    """
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)

# Manejo del error de archivo demasiado grande
@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Manejo del error de archivo demasiado grande.

    :param error: Error capturado
    :return: Mensaje de error y código de estado 413
    """
    return "El archivo es demasiado grande, el límite es de 16 MB.", 413

# Bloque de lógica de negocios

@app.route('/admin/guarda_cookies')
def editar():
    """
    Agrupa los logs por nivel y hora para contar el número de logs y guarda los resultados en un archivo JSON.

    :return: "Ok" si se completa correctamente.
    """
    grouped_logs = log_df.groupby(['Pais', 'Tag', 'Compra']).size().unstack(fill_value=0) 

    json_result = grouped_logs.to_json(orient='index')

    with open("templates/estadisticas.json", 'w') as f:
        f.write(json_result)
    
    return "Ok"

@app.route('/admin/recupera_Cookies')
def visualizar():
    """
    Carga los datos de un archivo JSON, los convierte a DataFrame, los ordena y los muestra en un template.

    :return: Template 'admin/estadistica.html' con los datos en formato HTML.
    """
    with open("templates/estadisticas.json", 'r', encoding='utf-8') as archivo:
        datajson = json.load(archivo)

    df = pd.DataFrame.from_dict(datajson, orient='index')
    df.index = pd.MultiIndex.from_tuples([eval(i) for i in df.index], names=["Pais", "Ciudad"])
    df = df.reset_index()
    df = df.sort_values(by=["Pais", "Ciudad"])

    table_html = df.to_html(index=False)
    return render_template('admin/estadistica.html', table_html=table_html)


@app.route('/admin/calcula_destinos')
def calcula_destinos():
    """
    Calcula los destinos usando la lógica de negocios definida en CalculosNegocios.

    :return: Resultado de la función calcula_destinos de CalculosNegocios.
    """
    return CalculosNegocios.calcula_destinos()

@app.route('/admin/calcula_usabilidad')
def calcula_usabilidad():
    """
    Calcula la usabilidad usando la lógica de negocios definida en CalculosNegocios.

    :return: Resultado de la función calculaUsabilidad de CalculosNegocios.
    """
    return CalculosNegocios.calculaUsabilidad()

@app.route('/admin/recupera_usabilidad')
def recupera_usabilidad():
    """
    Recupera los datos de usabilidad (pendiente de implementación).

    :return: Mensaje indicando que está pendiente de implementación.
    """
    return "pendiente"

@app.route('/admin/recupera_destinos')
def recupera_destinos():
    """
    Recupera los datos de destinos usando la lógica de negocios definida en CalculosNegocios.

    :return: Resultado de la función devulvem3 de CalculosNegocios.
    """
    return CalculosNegocios.devulvem3()

@app.route('/admin/guarda_usabilidad')
def guarda_usabilidad():
    """
    Guarda los datos de usabilidad (pendiente de implementación).

    :return: Mensaje indicando que está pendiente de implementación.
    """
    return "pendiente"

@app.route('/admin/guarda_destinos')
def guarda_destinos():
    """
    Guarda los datos de destinos (pendiente de implementación).

    :return: Mensaje indicando que está pendiente de implementación.
    """
    return "pendiente"

@app.route('/admin/buscar')
def buscar():
    """
    Busca alojamientos basados en criterios predefinidos.

    :return: JSON con los alojamientos encontrados.
    """
    criterios_busqueda = [
    {"tipo": "hotel"},
    {"fecha_entrada": "2024-08-01"},
    {"fecha_salida": "2024-11-12"}]

    criterios_busqueda = [{"nombre": "hotel Masnou"}]

    alojamientos_encontrados = buscar_alojamiento_por_criterios(criterios_busqueda)

    if alojamientos_encontrados:
        return jsonify(alojamientos_encontrados)
    else:
        return jsonify({})

@app.route('/admin/reservar')
def reservar():
    """
    Maneja la reserva de un alojamiento.

    :return: Mensaje de éxito si hay disponibilidad, de lo contrario mensaje de error.
    """
    libre = True
    if libre:
        return "Pase al proceso de compra por tarjeta"
    else:
        return "No hay disponibilidad para las fechas seleccionadas.", 400

@app.route('/admin/pagar')
def pagar():
    """
    Renderiza el formulario de pago.

    :return: Template 'admin/payment_form.html'
    """
    return render_template('admin/payment_form.html')

@app.route('/admin/process_payment', methods=['POST'])
def process_payment():
    """
    Procesa el pago con la información proporcionada.

    :return: Redirige al índice con un mensaje de éxito o error.
    """
    card_number = request.form['card_number']
    expiry_date = request.form['expiry_date']
    cvv = request.form['cvv']
    cardholder_name = request.form['cardholder_name']

    if card_number and expiry_date and cvv and cardholder_name:
        flash('Payment successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Payment failed. Please try again.', 'danger')
        return redirect(url_for('index'))

def guardapila(diccionario, nombre_archivo):
    """
    Guarda un diccionario en un archivo JSON.

    :param diccionario: Diccionario a guardar
    :param nombre_archivo: Nombre del archivo JSON
    """
    with open(nombre_archivo, 'w') as archivo:
        json.dump(diccionario, archivo, indent=4)

# Bloque de pila

@app.route('/admin/pilasuma/', methods=['GET'])
def pilasuma():
    """
    Añade una serie de operaciones a la pila y las guarda en un archivo JSON.

    :return: Mensaje indicando que se añadieron las operaciones a la pila.
    """
    afegir = [
    {
        "opcion": 5,
        "id_cliente": 123,
        "cliente": "Nombre del cliente",
        "empresa": "uber",
        "fecha": "2024-08-01 10:00"
    },
    {
        "opcion": 6,
        "id_cliente": 123,
        "cliente": "Nombre del cliente",
        "empresa": "uber",
        "conductor": "victor",
        "lugar_recogida": "Dirección de recogida",
        "lugar_destino": "Dirección de destino",
        "fecha": "2024-08-01 10:00"
    },
    {
        "opcion": 7,
        "id_cliente": 123,
        "conductor": "victor",
        "estado": "en camino"
    },
    {
        "opcion": 7,
        "id_cliente": 123,
        "conductor": "victor",
        "estado": "recogido"
    },
    {
        "opcion": 7,
        "id_cliente": 123,
        "conductor": "victor",
        "estado": "entregado"
    }
    ]
    guardapila(afegir, "pila.json")
    return "Añadidos pila"

@app.route('/admin/read_socket_data')
def read_socket_data():
    """
    Lee los datos recibidos por el socket y los devuelve en formato JSON.

    :return: JSON con los datos del socket.
    """
    return jsonify({"datos": socket_1.data_storage})

if __name__ == '__main__':
    app.run(debug=True)
