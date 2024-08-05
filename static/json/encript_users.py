# encrypt_users.py
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def load_keys():
    with open('public.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def encrypt_data(data, public_key):
    return public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def main():
    public_key = load_keys()

    # Leer el archivo JSON sin cifrar
    with open('static/json/users_plain.json', 'r') as f:
        users = json.load(f)

    # Convertir el diccionario a una cadena JSON
    users_json = json.dumps(users)

    # Cifrar la cadena JSON
    encrypted_users = encrypt_data(users_json, public_key)

    # Guardar el archivo JSON cifrado
    with open('static/json/users.json', 'wb') as f:
        f.write(encrypted_users)

    print("Usuarios cifrados y guardados en users.json")

if __name__ == '__main__':
    main()