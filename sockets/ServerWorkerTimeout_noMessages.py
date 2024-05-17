#!/usr/bin/env python3
import socket
import time

def handle_request(request):
    # Parse request and execute action
    args = request.split()
    action = args[0]
    arg1 = args[1]
    arg2 = args[2]
    
    # Perform action based on request
    # For example, you can print arguments and send a success message
    print("Received request:", action, arg1, arg2)
    # Execute some action based on the request

    # Send success message back to Java client
    return "SUCCESS"

def main():
    host = 'localhost'
    port = 8888
    timeout = 5  # Timeout in seconds

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.settimeout(timeout)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Python server listening on {host}:{port}")

        while True:
            try:
                conn, addr = server_socket.accept()
                with conn:
                    print('Connected by', addr)
                    request = conn.recv(1024).decode('utf-8')
                    if request:
                        response = handle_request(request)
                        conn.sendall(response.encode('utf-8'))
            except socket.timeout:
                print("Server timed out. Closing...")
                break

if __name__ == "__main__":
    main()

