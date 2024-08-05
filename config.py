import os
import pydoc

class Config:
    """
    Clase de configuración para la aplicación Flask.

    Atributos:
        SECRET_KEY (str): Clave secreta utilizada para la seguridad de la aplicación.
        JSON_USERS_FILE (str): Ruta al archivo JSON que contiene los datos de los usuarios.
        RSA_PRIVATE_KEY (str): Ruta al archivo que contiene la clave privada RSA.
        RSA_PUBLIC_KEY (str): Ruta al archivo que contiene la clave pública RSA.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JSON_USERS_FILE = 'static/json/users.json'
    RSA_PRIVATE_KEY = 'private.pem'
    RSA_PUBLIC_KEY = 'public.pem'
