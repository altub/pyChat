import socket
import threading

from tkinter import *

class client():
    def __init__(self):
        self.PORT = 5000
        self.HOST = '127.0.0.1'
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Window = Tk()
        self.Window.geometry("400x600")
        self.labelTop = Label(self.Window, bg = 'green', height = 5)
        self.labelTop.place(relwidth = 1)
        self.entryName = Entry(self.labelTop, bg = 'white')
        self.entryName.place(relwidth = 0.40, relheight = 0.3, relx = 0.10, rely = 0.03)
        self.entryName.focus()
        self.startButton = Button(self.labelTop, text = "Start chat", command = self.startCli)
        self.startButton.place(relx = 0.5, rely = 0.005)

        self.labelBottom = Label(self.Window, bg = 'red', height = 5)
        self.labelBottom.place(relwidth = 1, rely = .75)
        self.entryMessage = Entry(self.labelBottom, bg = 'white')
        self.entryMessage.place(relwidth = 0.7, relheight = 0.3, relx = 0.1, rely = 0.03)
        self.sendButton = Button(self.labelBottom, text = "Start chat", command = lambda : self.sending(self.entryMessage.get()))
        self.sendButton.place(relx = 0.7, rely = 0.005)

        self.Window.protocol("WM_DELETE_WINDOW", self.stop)
        self.Window.mainloop()
        self.Window.quit()

    def sending(self, data):
        self.entryMessage.delete(0, END)
        snd = threading.Thread(target = self.sendData(data))
        snd.start()

    def stop(self):
        self.running = False
        self.Window.destroy()
        self.sock.close()
        exit(0)

    def startCli(self):
        self.sock.connect(self.ADDRESS)
        self.name = self.entryName.get()
        rcv = threading.Thread(target = self.handleRecv)
        rcv.start()

    def handleRecv(self):
        SIZE = 1024
        while True:
            try:
                data = self.sock.recv(SIZE).decode(self.FORMAT)
                if(data == 'NAME'):
                    self.sock.send(self.name.encode(self.FORMAT))
                elif(data):
                    print(data)
            except:
                print("An error occurred")
                self.sock.close()
                break

    def sendData(self, data):
        self.sock.send((f"{self.name}: " + data).encode(self.FORMAT))


if __name__ == "__main__":
    c = client()