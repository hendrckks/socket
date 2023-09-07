import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_host(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
               connected = False

            print(f"[{addr}] {msg}")
 
    conn.close()    

           
def start():
    server.listen()
    print(f"[SERVER] server is listening in {SERVER}")
    while True :
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_host, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[SERVER] IS STARTING....")
start()
