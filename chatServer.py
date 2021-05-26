import socket

import threading

class threadServer():
    def __init__(self):
        self.PORT = 5000
        self.HOST = ''
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.SIZE = 1024
        self.clients, self.names = [], []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDRESS)
        self.startSer()

    def startSer(self):
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            self.clients.append(client)
            client.send('NAME'.encode(self.FORMAT))
            name = client.recv(self.SIZE).decode(self.FORMAT)
            self.names.append(name)
            print(f"{name}")
            self.sendData(f"{name} has joined the chat.".encode(self.FORMAT))
            thread = threading.Thread(target = self.handleReq, args = (client, address))
            thread.start()

    def handleReq(self, client, address):
        print(f"Connected to : {str(address)}")
        while True:
            try:
                data = client.recv(self.SIZE)
                if(data):
                    self.sendData(data)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                del self.names[index]
                self.sendData(f"{name} has left the chat.".encode(self.FORMAT))
                break
    def sendData(self, data):
        for client in self.clients:
            client.send(data)
        

if __name__ == "__main__":
    tS = threadServer()