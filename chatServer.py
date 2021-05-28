import socket

import threading

class threadServer():
    def __init__(self):
        self.PORT = 5000
        self.HOST = ''
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.SIZE = 1024
        self.clients, self.names, self.rooms = [], [], []
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
            client.send('ROOM'.encode(self.FORMAT))
            room = client.recv(self.SIZE).decode(self.FORMAT)
            self.rooms.append(room)
            print(f"{name}")
            self.sendData(f"{name} has joined the chat.".encode(self.FORMAT), room)
            thread = threading.Thread(target = self.handleReq, args = (client, address))
            thread.start()

    def handleReq(self, client, address):
        print(f"Connected to : {str(address)}")
        while True:
            try:
                index = self.clients.index(client)
                room = self.rooms[index]
                data = client.recv(self.SIZE)
                if(data.decode(self.FORMAT) == "UISDH84;E4T49HAO4Y;Y9;ATYS;YH;HFG;9SS;4H9GI"):
                    self.chngRoom(client)
                elif(data):
                    self.sendData(data, room)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                room = self.rooms[index]
                del self.rooms[index]
                del self.names[index]
                self.sendData(f"{name} has left the chat.".encode(self.FORMAT), room)
                break

    def chngRoom(self, client):
        client.send('ROOM'.encode(self.FORMAT))
        data = client.recv(self.SIZE).decode(self.FORMAT)
        index = self.clients.index(client)
        room = self.rooms[index]
        if(data == room):
            return
        else:
            name = self.names[index]
            self.sendData(f"{name} has left the chat.".encode(self.FORMAT), room)
            self.rooms[index] = data
            self.sendData(f"{name} has joined the chat.".encode(self.FORMAT), data)
            client.send(f"\nYou joined room {data}".encode(self.FORMAT))

    def sendData(self, data, chatRm):
        for x, room in enumerate(self.rooms):
            if room == chatRm:
                client = self.clients[x]
                client.send(data)
        

if __name__ == "__main__":
    tS = threadServer()