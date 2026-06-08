import socket

HOST = "localhost"
PORT = 5000

while True:

    print("\n--- MENU ---")
    print("1. Crear tarea")
    print("2. Ver tareas")
    print("3. Borrar tarea")
    print("4. Salir")

    op = input("Opción: ")
    if op == "1":
        titulo = input("Título: ")
        mensaje = f"CREAR;{titulo}"
    elif op == "2":
        mensaje = "VER"
    elif op == "3":
        id_tarea = input("ID de la tarea: ")
        mensaje = f"BORRAR;{id_tarea}"
    elif op == "4":
        break
    else:
        continue
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    s.connect((HOST, PORT))
    s.send(mensaje.encode())
    respuesta = s.recv(4096).decode()
    print("\nRespuesta:")
    print(respuesta)
    s.close()