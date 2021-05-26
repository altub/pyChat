import socket

import threading

class threadServer():
    def __init__(self):
        self.PORT = 5000
        self.HOST = ''
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDRESS)
        self.startSer()

    def startSer(self):
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            thread = threading.Thread(target = self.handleReq, args = (client, address))
            thread.start()

    def handleReq(self, client, address):
        SIZE = 1024
        print(f"Connected to : {str(address)}")
        while True:
            try:
                data = client.recv(SIZE)
                if(data):
                    self.sendData(client, data)
            except:
                client.close()
                break
    def sendData(self, client, data):
        client.send(("You sent : ".encode(self.FORMAT) + data))

if __name__ == "__main__":
    tS = threadServer()