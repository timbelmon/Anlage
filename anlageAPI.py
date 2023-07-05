import socket
import anlageTurnTableController

HOST = '0.0.0.0'
PORT = 1339

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

object_dict = {}

while True:
    print("Server listening on {}:{}".format(HOST, PORT))

    client_socket, client_address = server_socket.accept()
    print("Connected to client:", client_address)

    client_socket.sendall("Bitte IP-Adresse eingeben.".encode())
    ip = client_socket.recv(1024).decode()
    ip = ""

    if ip != "":
        print("Received IP-Address:", ip)
        if ip in object_dict:
            anlageTurntable = object_dict[ip]
        else:
            anlageTurntable = anlageTurnTableController.AnlageController(ip)
            object_dict[ip] = anlageTurntable

        client_socket.sendall("Verbunden.".encode())


    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print("Received message:", message)
        if message != "/disconnect":
            response = "Transmission received."
            if message == "ejectB":
                response = "Ejected part"
                anlageTurntable.ejector_b("eject")
            elif message == "ejectA":
                response = "Ejected part."
                anlageTurntable.ejector_a("eject")
            elif message == "turn":
                response = "Turned."
                anlageTurntable.turn_turn_table()
            elif message == "borePart":
                response = "Bored part."
                anlageTurntable.bore_part()
            elif message == "start":
                respone = "Starting Default-Routine."
                anlageTurntable.default_behaviour(True)
            elif message == "stop":
                respone = "Stopping Default-Routine."
                anlageTurntable.default_behaviour(False)
            elif message == "checkPart":
                if anlageTurntable.check_part() == True:
                    response = "Part Check: True"
                else:
                    response = "Part Check: False"
            client_socket.sendall(response.encode())
        elif message == "/close":
            client_socket.close()
            server_socket.close()
