import socket
import threading
from queue import Queue

HOST = "localhost"
PORT = 5000

cola = Queue()

tareas = []
lock = threading.Lock()

# -------------------
# WORKERS
# -------------------

def worker(nombre):

    while True:

        cliente, mensaje = cola.get()

        partes = mensaje.split(";", 1)

        comando = partes[0]

        if comando == "CREAR":

            titulo = partes[1]

            with lock:
                tareas.append(titulo)

            respuesta = f"{nombre}: tarea creada"

        elif comando == "VER":

            with lock:

                if tareas:
                    respuesta = "\n".join(tareas)
                else:
                    respuesta = "No hay tareas"

        else:

            respuesta = "Comando inválido"

        cliente.send(respuesta.encode())

        cliente.close()

        cola.task_done()


# -------------------
# SERVIDOR
# -------------------

def servidor():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))

    s.listen()

    print("Servidor escuchando...")

    threading.Thread(
        target=worker,
        args=("Worker-1",),
        daemon=True
    ).start()

    threading.Thread(
        target=worker,
        args=("Worker-2",),
        daemon=True
    ).start()

    while True:

        cliente, addr = s.accept()

        mensaje = cliente.recv(1024).decode()

        cola.put((cliente, mensaje))


servidor()