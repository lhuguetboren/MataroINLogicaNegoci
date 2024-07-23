import asyncio
import aiohttp
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
#from  alojamientos import Alojamientos, sessionmaker

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

class Viaje:
    """
    Clase que representa un viaje.

    Attributes:
        hotel (str): Nombre del hotel.
        fecha_inicio (str): Fecha de inicio de la reserva.
        fecha_fin (str): Fecha de fin de la reserva.
        habitaciones (int): Número de habitaciones reservadas.
    """
    def __init__(self, hotel, fecha_inicio, fecha_fin, habitaciones):
        self.hotel = hotel
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.habitaciones = habitaciones

@app.route('/api/verificar_disponibilidad', methods=['POST'])
def api_verificar_disponibilidad():
    """
    Endpoint para verificar la disponibilidad de un hotel.

    Returns:
        json: Mensaje cifrado indicando la disponibilidad.
    """
    data = request.json
    encrypted_message = data.get('message')
    
    decrypted_message = decrypt_message(
        bytes.fromhex(encrypted_message),
        private_key
    )

    data = json.loads(decrypted_message)
    hotel_id = data.get('hotel_id')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    habitaciones = data.get('habitaciones')

    # Aquí podrías realizar la lógica real de verificación de disponibilidad
    # Por ahora, simplemente retornamos que siempre hay disponibilidad
    encrypted_response = encrypt_message(json.dumps({'disponible': True}).encode('utf-8'), public_key)
    return jsonify(message=encrypted_response.hex())

class VerificadorDisponibilidad:
    """
    Clase para manejar las solicitudes asincrónicas de verificación de disponibilidad.

    Attributes:
        base_url (str): URL base del servidor.
        public_key (rsa.RSAPublicKey): Clave pública para cifrar los mensajes.
    """
    def __init__(self, base_url, public_key):
        self.base_url = base_url
        self.public_key = public_key

    async def verificar(self, hotel_id, fecha_inicio, fecha_fin, habitaciones):
        """
        Verifica la disponibilidad de un hotel de manera asíncrona.

        Args:
            hotel_id (str): ID del hotel.
            fecha_inicio (str): Fecha de inicio de la reserva.
            fecha_fin (str): Fecha de fin de la reserva.
            habitaciones (int): Número de habitaciones reservadas.

        Returns:
            bool: Disponibilidad del hotel.
        """
        message = json.dumps({
            'hotel_id': hotel_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'habitaciones': habitaciones
        }).encode('utf-8')
        
        encrypted_message = encrypt_message(message, self.public_key)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.base_url}/api/verificar_disponibilidad', json={
                'message': encrypted_message.hex()
            }) as response:
                response_data = await response.json()
                decrypted_response = decrypt_message(
                    bytes.fromhex(response_data['message']),
                    private_key
                )
                return json.loads(decrypted_response)['disponible']

@app.route('/')
def index():
    """
    Ruta principal que renderiza el formulario para agregar un viaje al carrito.

    Returns:
        str: Render de la plantilla index.html.
    """
    return render_template('index.html')

@app.route('/add_to_cart', methods=['POST'])
async def add_to_cart():
    """
    Agrega un viaje al carrito después de verificar la disponibilidad.

    Returns:
        str: Redirección a la vista del carrito o mensaje de error.
    """
    hotel = request.form['hotel']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    habitaciones = request.form['habitaciones']

    verificador = VerificadorDisponibilidad(request.host_url.rstrip('/'), public_key)
    disponibilidad = await verificador.verificar(hotel, fecha_inicio, fecha_fin, habitaciones)
    
    if disponibilidad:
        viaje = Viaje(hotel, fecha_inicio, fecha_fin, habitaciones)
        
        if 'cart' not in session:
            session['cart'] = []
        
        session['cart'].append(viaje.__dict__)
        return redirect(url_for('view_cart'))
    else:
        return "No hay disponibilidad para las fechas seleccionadas.", 400

@app.route('/cart')
def view_cart():
    """
    Muestra el contenido del carrito.

    Returns:
        str: Render de la plantilla cart.html.
    """

    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)


@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    """
    Elimina un viaje del carrito por su índice.

    Args:
        index (int): Índice del viaje a eliminar.

    Returns:
        str: Redirección a la vista del carrito.
    """
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)
