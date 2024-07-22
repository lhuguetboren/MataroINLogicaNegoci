from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import os
from clasesb import session, Biblioteca, get_current_time_in_spain, Tag, TagsRelacion


# Lista para almacenar los archivos subidos temporalmente
uploaded_files = []

# Inicialización de la aplicación Flask
app = Flask(__name__)
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

# Ruta principal para mostrar el formulario de subida de archivos
@app.route("/")
def upload_file():
    """
    Muestra el formulario de subida de archivos y lista los archivos ya subidos.

    :return: Renderiza el template 'formulariob.html'
    """
    photos = os.listdir(app.config['PHOTO_FOLDER'])
    videos = os.listdir(app.config['VIDEO_FOLDER'])
    brochures = os.listdir(app.config['BROCHURE_FOLDER'])

    # Obtener todas las etiquetas de la base de datos
    tags = session.query(Tag).all()

    # Comprobar si se solicita mostrar la opción de eliminar un archivo
    show_delete = request.args.get('show_delete')

    delete_file_info = None
    if show_delete:
        for file in uploaded_files:
            if file['filename'] == show_delete:
                delete_file_info = file
                break

    return render_template('formulariob.html', photos=photos, videos=videos, brochures=brochures, uploaded_files=uploaded_files, delete_file_info=delete_file_info, tags=tags)

# Ruta para manejar la subida de archivos
@app.route("/uploader", methods=['POST'])
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
                # Obtener la duración del video
                video = VideoFileClip(filepath)
                duration = video.duration
                video.reader.close()  
                video.audio.reader.close_proc() 
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
        tags_seleccionados = [session.query(Tag).get(int(tag_id)) for tag_id in tag_ids]
        
        # Crear una nueva entrada en la base de datos
        nueva_entrada = Biblioteca(
            tipo=tipo,
            nombre=nombre,
            descripcion=descripcion,
            filename=filename,
            duracion=duration,
            formato=file_format,
            tags_relacion=[TagsRelacion(origen="biblioteca", id_tag=tag.id) for tag in tags_seleccionados]
        )

        # Guardar la nueva entrada en la base de datos
        session.add(nueva_entrada)
        session.commit()

        return redirect(url_for('upload_file'))

# Ruta para editar archivos
@app.route("/edit/<folder>/<filename>", methods=['GET', 'POST'])
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

    return render_template('editb.html', folder=folder, filename=filename, file=file_entry)

# Ruta para eliminar archivos
@app.route("/delete/<folder>/<filename>", methods=['POST'])
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
@app.route('/uploads/<folder>/<filename>')
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

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True)


