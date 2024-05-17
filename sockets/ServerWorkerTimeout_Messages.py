import socket
import time
import threading
from ecuapass_server import EcuServer 

def handle_request(conn):
    while True:
        try:
            request = conn.recv(1024).decode('utf-8')
            if request:
                response = handle_request_action(request)
                conn.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            print("Connection closed.")
            break

def handle_request_action(request):
    args    = request.split()
    service = args[0]
    data1   = args[1]
    data2   = args[2]
    
	printx ("Servicio  : ", service, flush=True)
	printx ("Dato 1    : ", data1, flush=True)
	printx ("Dato 2    : ", data2, flush=True)

	# Call your existing script's function to process the file
	result = None
	if (service == "doc_processing"):
		result = EcuServer.analizeOneDocument (docFilepath=data1, runningDir=data2)

	elif (service == "bot_processing"):
		result = EcuServer.botProcessing (jsonFilepath=data1, runningDir=data2)

	elif (service == "codebin_transmit"):
		result = EcuServer.codebin_transmit (workingDir=data1, codebinFieldsFile=data2)

	elif (service == "ecuapassdocs_transmit"):
		result = EcuServer.ecuapassdocs_transmit (workingDir=data1, ecuapassdocsFieldsFile=data2)

	elif (service == "open_ecuapassdocs_URL"):
		EcuServer.openEcuapassdocsURL (url=data1)

	elif (service == "stop"):
		EcuServer.stop_server ()

	elif (service == "send_feedback"):
		EcuFeedback.sendFeedback (zipFilepath=data1, docFilepath=data2)
		result = "true"

	elif (service == "is_running"):
		result = "true"

	else:
		result = f">>> Servicio '{service}' no disponible."

    return "SUCCESS"

def send_notifications(conn):
    while True:
        time.sleep(5)  # Sending notification every 5 seconds
        notification = "Notification from server"
        conn.sendall(notification.encode('utf-8'))

def main():
    host = 'localhost'
    port = 8888
    timeout = 60  # Timeout in seconds

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.settimeout(timeout)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Python server listening on {host}:{port}")

        try:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")

            # Start a thread to handle the client connection
            client_thread = threading.Thread(target=handle_request, args=(conn,))
            client_thread.start()

            # Start a thread to send notifications
            notification_thread = threading.Thread(target=send_notifications, args=(conn,))
            notification_thread.start()

            # Wait for the client thread to finish
            client_thread.join()
        except socket.timeout:
            print("Server timed out. Closing...")
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()

