from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import pydoc

def generate_rsa_keys():
    """
    Genera un par de claves RSA (privada y pública) y las guarda en archivos PEM.

    La clave privada se guarda en 'private.pem' y la clave pública en 'public.pem'.
    """
    # Generar la clave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Generar la clave pública a partir de la clave privada
    public_key = private_key.public_key()

    # Serializar la clave privada a formato PEM
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serializar la clave pública a formato PEM
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Guardar la clave privada en un archivo
    with open('private.pem', 'wb') as f:
        f.write(pem_private_key)

    # Guardar la clave pública en un archivo
    with open('public.pem', 'wb') as f:
        f.write(pem_public_key)

if __name__ == "__main__":
    generate_rsa_keys()
