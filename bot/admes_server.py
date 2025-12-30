"""
Admes TCP server for handling bot queries
"""

import socket
import threading
from typing import Optional

# Global socket streams
socket_in: Optional[socket.socket] = None
socket_out: Optional[socket.socket] = None
server_socket: Optional[socket.socket] = None
clients: list = []


def init_admes_server(port=12102):
    """Initialize and start the Admes TCP server"""
    global server_socket

    def run_server():
        global server_socket, socket_in, socket_out, clients

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen(5)
            print(f"Admes server started at port {port}!")

            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    print(
                        f"New client joined at {client_address[0]}, port {client_address[1]}"
                    )
                    clients.append(client_socket)

                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=handle_client,
                        args=(client_socket, client_address),
                        daemon=True,
                    )
                    client_thread.start()
                except Exception as e:
                    if server_socket:
                        print(f"Error accepting client: {e}")
        except Exception as e:
            print(f"Error starting Admes server: {e}")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()


def handle_client(client_socket: socket.socket, client_address):
    """Handle individual client connection"""
    global socket_in, socket_out

    try:
        # Set this client as the active connection
        socket_in = client_socket
        socket_out = client_socket

        # Keep connection alive
        while True:
            if client_socket.fileno() == -1:  # Socket closed
                break
            try:
                # Wait for data (with timeout to check if socket is still alive)
                client_socket.settimeout(1.0)
                data = client_socket.recv(1024)
                if not data:
                    break
            except socket.timeout:
                continue
            except Exception:
                break
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        if socket_in == client_socket:
            socket_in = None
        if socket_out == client_socket:
            socket_out = None
        try:
            client_socket.close()
        except:
            pass
        print(f"Client {client_address} disconnected")


def send_query(query: str) -> Optional[str]:
    """Send query to Admes server and get response"""
    global socket_in, socket_out

    if socket_out is None or socket_in is None:
        return None

    try:
        # Send query
        message = f"Question: {query}\n\nReply: "
        socket_out.sendall(message.encode("utf-8"))

        # Wait for response
        socket_in.settimeout(10.0)  # 10 second timeout
        response = socket_in.recv(4096).decode("utf-8")

        # Clean up response
        response = response.strip()
        if not response:
            return None

        return response
    except socket.timeout:
        return None
    except Exception as e:
        print(f"Error communicating with Admes server: {e}")
        return None


def close_server():
    """Close the Admes server"""
    global server_socket, socket_in, socket_out, clients

    # Close all client connections
    for client in clients[:]:
        try:
            client.close()
        except:
            pass
    clients.clear()

    # Close server socket
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
        server_socket = None

    socket_in = None
    socket_out = None
