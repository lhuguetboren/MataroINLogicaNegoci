import socket
import threading
import pydoc

# Almacenamiento global para los datos recibidos
data_storage = []

def handle_client(conn, addr):
    """
    Maneja la conexión con un cliente.

    Lee los datos enviados por el cliente y los almacena en data_storage.
    Cierra la conexión cuando no se reciben más datos.

    :param conn: Objeto de conexión de socket.
    :param addr: Dirección del cliente.
    """
    print(f"Conexión establecida con {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data_storage.append(data)
    conn.close()

def start_server():
    """
    Inicia el servidor de socket.

    El servidor escucha en el host y puerto especificados, acepta conexiones entrantes y
    crea un hilo para manejar cada cliente.
    """
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor de socket escuchando en {host}:{port}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
