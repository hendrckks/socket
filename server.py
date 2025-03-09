import socket
import threading
import sys
from datetime import datetime

# Constants
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Initialize server socket
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    server.bind(ADDR)
except socket.error as e:
    print(f"[ERROR] Failed to initialize server: {e}")
    sys.exit(1)

def handle_host(conn, addr):
    """Handle individual client connections"""
    print(f"[NEW CONNECTION] {addr} connected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    connected = True
    while connected:
        try:
            # Receive message length
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:  # Client disconnected
                break
                
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECT] {addr} disconnected")
            else:
                print(f"[{addr[0]}:{addr[1]}] {msg}")
                
            # Echo message back to client (optional)
            conn.send(f"Message received: {msg}".encode(FORMAT))
            
        except (ConnectionResetError, ValueError) as e:
            print(f"[ERROR] Connection with {addr} lost: {e}")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error with {addr}: {e}")
            break
            
    conn.close()
    print(f"[CONNECTION CLOSED] {addr}")

def start():
    """Start the server and handle incoming connections"""
    try:
        server.listen(5)  # Allow up to 5 queued connections
        print(f"[SERVER] Listening on {SERVER}:{PORT}")
        
        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_host, args=(conn, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
                
            except Exception as e:
                print(f"[ERROR] Error accepting connection: {e}")
                
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        server.close()

def main():
    """Main function to start the server"""
    print(f"[SERVER] Starting on {SERVER}:{PORT}...")
    start()

if __name__ == "__main__":
    main()
