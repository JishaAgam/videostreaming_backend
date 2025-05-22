# app/sockets.py
import socket
import threading

# This holds the currently running socket threads (so we don’t start duplicates)
running_sockets = {}

def socket_server(port, domain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen()
    print(f"[Socket] Listening on port {port} for {domain}")
    
    while True:
        conn, addr = s.accept()
        print(f"[Socket] Connection from {addr} on port {port}")
        message = f"Hello from socket server for {domain} on port {port}\n"
        conn.sendall(message.encode())
        conn.close()

def start_socket_for_domain(domain, port):
    if domain in running_sockets:
        print(f"[Socket] Socket already running for {domain}")
        return
    
    t = threading.Thread(target=socket_server, args=(port, domain), daemon=True)
    t.start()
    running_sockets[domain] = {
        "port": port,
        "thread": t
    }
    print(f"[Thread] Started socket for {domain} on port {port}")
