import matplotlib.pyplot as plt
from pythonosc import dispatcher, osc_server
import threading

# Global variables
board="/board0"
#ip="172.25.7.255"
ip="0.0.0.0"
values = [0.0, 0.0, 0.0,0.0]
running = True



# Function to handle incoming OSC messages on /board0
def handle_board0(unused_addr, *args):
    global values
    if len(args) == 4 and all(isinstance(arg, float) for arg in args):
        values = list(args)
        #print(f"Received values: {values}")
    else:
        print(f"Invalid message format: {args}")

# Setting up the OSC server
dispatcher = dispatcher.Dispatcher()
dispatcher.map(board, handle_board0)

server = osc_server.ThreadingOSCUDPServer((ip, 54321), dispatcher)
print("Serving on {}".format(server.server_address),board)

# Function to update the plot
def live_plotter():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    
    # Set y-axis limits here (min, max)
    ax.set_ylim([0, 100])  

    # Button click event handler
    def on_close(event):
        global running
        running = False

    fig.canvas.mpl_connect('close_event', on_close)

    while running:
        plt.pause(0.1)
        ax.clear()
        ax.bar(['Value0', 'Value1', 'Value2','Value3'], values)
        ax.set_ylim([-100, 100])  # Maintain y-axis limits after clearing the axes
        plt.draw()

    plt.close(fig)

# Running the OSC server in a separate thread
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

# Running the plotter in the main thread
live_plotter()

# After closing the plot window
server.shutdown()
server_thread.join()
print("Server and plot closed.")
