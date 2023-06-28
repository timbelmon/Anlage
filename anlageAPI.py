import socket
import anlageTurnTableController

anlageTurntable = anlageTurnTableController.AnlageController("192.168.200.231")

HOST = '0.0.0.0'  
PORT = 1337

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

while True:
    print("Server listening on {}:{}".format(HOST, PORT))

    client_socket, client_address = server_socket.accept()
    print("Connected to client:", client_address)

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
            elif message == "checkPart": 
                if anlageTurntable.check_part() == True:
                    response = "Part Check: True"
                else:
                    response = "Part Check: False"
            client_socket.sendall(response.encode())
        elif message == "/disconnect":
            client_socket.close()
            server_socket.close()
