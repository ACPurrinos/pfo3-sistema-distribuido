import socket
import threading
import sqlite3
from queue import Queue

HOST = "localhost"
PORT = 5000
DATABASE = "tareas.db"

cola = Queue()

db_lock = threading.Lock()

# -----------------------
# BASE DE DATOS
# -----------------------

def crear_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


# -----------------------
# WORKERS
# -----------------------

def worker(nombre):

    while True:
        cliente, mensaje = cola.get()
        try:
            print(f"{nombre} procesando: {mensaje}")
            partes = mensaje.split(";", 1)
            comando = partes[0]
            if comando == "CREAR":
                titulo = partes[1]

                with db_lock:
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO tareas(titulo) VALUES (?)",
                        (titulo,)
                    )
                    conn.commit()
                    conn.close()
                respuesta = f"{nombre}: tarea creada"

            elif comando == "VER":
                with db_lock:
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT id, titulo FROM tareas"
                    )
                    tareas = cursor.fetchall()
                    conn.close()
                if tareas:
                    respuesta = "\n".join(
                        f"{id} - {titulo}"
                        for id, titulo in tareas
                    )
                else:
                    respuesta = "No hay tareas"
            elif comando == "BORRAR":
                id_tarea = int(partes[1])
                with db_lock:
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM tareas WHERE id = ?",
                        (id_tarea,)
                    )
                    eliminadas = cursor.rowcount
                    conn.commit()
                    conn.close()
                if eliminadas:
                    respuesta = f"{nombre}: tarea eliminada"
                else:
                    respuesta = "No existe esa tarea"
            else:
                respuesta = "Comando inválido"
            cliente.send(respuesta.encode())
        except Exception as e:
            cliente.send(
                f"Error: {str(e)}".encode()
            )
        finally:
            cliente.close()
            cola.task_done()

# -----------------------
# CLIENTES
# -----------------------

def atender_cliente(cliente):
    try:
        mensaje = cliente.recv(1024).decode()
        cola.put((cliente, mensaje))
    except:
        cliente.close()

# -----------------------
# SERVIDOR
# -----------------------

def servidor():
    crear_db()
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
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    while True:
        cliente, addr = s.accept()
        print(f"Conexión desde {addr}")
        threading.Thread(
            target=atender_cliente,
            args=(cliente,),
            daemon=True
        ).start()


servidor()