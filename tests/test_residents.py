from pythonosc import dispatcher
from pythonosc import osc_server
import threading

def handle_osc_message(unused_addr, args, *osc_args):
    print(f"Received OSC message: {osc_args}")

# Set up the dispatcher to handle incoming messages
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/board8", handle_osc_message, "Message Argument")

# Set the IP address and port for the OSC server (listener)
ip = "172.25.7.255"  # Listening on all available interfaces
port = 54321  # The port you want to listen on

# Create and start the OSC server
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serving on {}".format(server.server_address))

# Run the server in a separate thread to keep it non-blocking
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
