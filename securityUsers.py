import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from flask_login import UserMixin
import pydoc

class User(UserMixin):
    """
    Clase que representa a un usuario en la aplicación.

    Hereda de UserMixin para integrarse con Flask-Login.

    :param id: ID del usuario.
    :param username: Nombre de usuario.
    :param password: Contraseña del usuario.
    """
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def load_keys():
    """
    Carga las claves privada y pública RSA desde archivos PEM.

    :return: Una tupla con la clave privada y la clave pública.
    """
    with open('private.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open('public.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    return private_key, public_key

def encrypt_data(data, public_key):
    """
    Cifra los datos utilizando la clave pública RSA.

    :param data: Datos a cifrar en forma de cadena de texto.
    :param public_key: Clave pública utilizada para el cifrado.
    :return: Datos cifrados en forma de bytes.
    """
    return public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_data(ciphertext, private_key):
    """
    Descifra los datos utilizando la clave privada RSA.

    :param ciphertext: Datos cifrados en forma de bytes.
    :param private_key: Clave privada utilizada para el descifrado.
    :return: Datos descifrados en forma de cadena de texto.
    """
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

def save_users(users, public_key):
    """
    Cifra y guarda la información de los usuarios en un archivo JSON.

    :param users: Diccionario con los datos de los usuarios.
    :param public_key: Clave pública utilizada para cifrar los datos.
    """
    encrypted_users = encrypt_data(json.dumps(users), public_key)
    with open('static/json/users.json', 'wb') as f:
        f.write(encrypted_users)

def load_users(private_key):
    """
    Carga y descifra la información de los usuarios desde un archivo JSON.

    :param private_key: Clave privada utilizada para descifrar los datos.
    :return: Diccionario con los datos de los usuarios.
    """
    try:
        with open('static/json/users.json', 'rb') as f:
            encrypted_users = f.read()
            decrypted_users = decrypt_data(encrypted_users, private_key)
            return json.loads(decrypted_users)
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

# Cargar las claves y los usuarios al inicio del programa
private_key, public_key = load_keys()
users = load_users(private_key)
