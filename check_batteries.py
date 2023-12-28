import socket
import re

def start_server(port=54321):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    s.bind(('', port))
    print(f"Listening on port {port}...")

    # Listen for incoming connections
    s.listen()

    while True:
        # Accept a connection
        client_socket, addr = s.accept()

        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')

            # Regular expression to parse the request path and array
            match = re.search(r'/board(\d+).*\[(.*?)\]', data)
            if match:
                board_number = int(match.group(1))
                if 0 <= board_number <= 12:
                    # Extract the array and the fourth value
                    array_values = match.group(2).split(',')
                    if len(array_values) >= 4:
                        fourth_value = array_values[3].strip()
                        print(f"/board{board_number}: {fourth_value}", end='\r')
                    else:
                        print("Array does not have enough elements.")
                else:
                    print("Board number out of range.")
            else:
                print("Invalid request format.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the connection
            client_socket.close()

# Start the server
start_server()  # Uncomment this line to run the server

# Note: Running this server in the current environment won't work because it's an isolated sandbox.
# Please run this script in your local Python environment.
