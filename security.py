from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pydoc

import asyncio

# Generar claves RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()



def encrypt_message(message, public_key):
    """
    Cifra un mensaje utilizando la clave pública RSA.

    Args:
        message (bytes): Mensaje a cifrar.
        public_key (rsa.RSAPublicKey): Clave pública para cifrar el mensaje.

    Returns:
        bytes: Mensaje cifrado.
    """
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_message(encrypted_message, private_key):
    """
    Descifra un mensaje utilizando la clave privada RSA.

    Args:
        encrypted_message (bytes): Mensaje cifrado.
        private_key (rsa.RSAPrivateKey): Clave privada para descifrar el mensaje.

    Returns:
        bytes: Mensaje descifrado.
    """
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

