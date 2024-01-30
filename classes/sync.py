import socket

class sync():

    mode="master"
    destination="255.255.255.255"

    def __init__(self,mode="master"):
        self.sock = self.init_socket()

        self.mode=mode

        if self.mode=="master":
            #master
           
            self.socket_enable_broadcast()
            self.socket_connect(self.destination)

       
        else:
            #slave
            self.read_position_master()
            #self.set_playlist_index()


    def init_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock.bind(('0.0.0.0', PORT))
        return sock