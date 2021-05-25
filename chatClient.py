import socket
import threading

class client():
    def __init__(self):
        self.PORT = 5000
        self.HOST = '127.0.0.1'
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.startCli()

    def startCli(self):
        self.sock.connect(self.ADDRESS)
        rcv = threading.Thread(target = self.handleRecv)
        rcv.start()
        snd = threading.Thread(target = self.sendData)
        snd.start()

    def handleRecv(self):
        SIZE = 1024
        while True:
            try:
                data = self.sock.recv(SIZE).decode(self.FORMAT)
                if(data):
                    print(data)
            except:
                print("An error occurred")
                self.sock.close()
                break

    def sendData(self):
        while True:
            data = input("Enter your message: ")
            self.sock.send(data.encode(self.FORMAT))
            end = input('End connection(y/n)? ')
            if(end == 'y'):
                self.sock.close()
                break


if __name__ == "__main__":
    c = client()