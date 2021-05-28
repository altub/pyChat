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
        self.Window.resizable(width = False, height = False)
        self.Window.geometry("400x600")
        self.labelTop = Label(self.Window, bg = 'green', height = 5)
        self.labelTop.place(relwidth = 1)
        self.entryName = Entry(self.labelTop, bg = 'white')
        self.entryName.place(relwidth = 0.40, relheight = 0.3, relx = 0.10, rely = 0.03)
        self.entryName.focus()
        self.startButton = Button(self.labelTop, text = "Start chat", command = self.startCli)
        self.startButton.place(relx = 0.5, rely = 0.005)

        self.textDisp = Text(self.Window, width = 375, height = 300)
        self.textDisp.place(relwidth = 1, relheight = 0.6, rely = 0.06)
        
        textScrollbar = Scrollbar(self.textDisp)
        textScrollbar.place(relheight = 1, relx = 0.960)
        textScrollbar.config(command = self.textDisp.yview)
        self.textDisp.config(yscrollcommand = textScrollbar.set, state = DISABLED)

        rooms = [1,2,3,4,5]
        self.currentRoom = StringVar(self.labelTop)
        self.currentRoom.set(1)
        self.currentRoom.trace('w', self.changeRoom)
        self.roomOptions = OptionMenu(self.labelTop, self.currentRoom, *rooms)
        self.roomOptions.place(anchor = NW)
        

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

        self.entryName.destroy()
        self.startButton.destroy()

        rcv = threading.Thread(target = self.handleRecv)
        rcv.start()

    def handleRecv(self):
        SIZE = 1024
        while True:
            try:
                data = self.sock.recv(SIZE).decode(self.FORMAT)
                if(data == 'NAME'):
                    self.sock.send(self.name.encode(self.FORMAT))
                elif(data == 'ROOM'):
                    self.sock.send(self.currentRoom.get().encode(self.FORMAT))
                elif(data):
                    self.textDisp.config(state = NORMAL)
                    self.textDisp.insert(END, data + "\n")
                    self.textDisp.config(state = DISABLED)
                    self.textDisp.see(END)
            except:
                print("An error occurred")
                self.sock.close()
                break

    def changeRoom(self, *args):
        self.sock.send("UISDH84;E4T49HAO4Y;Y9;ATYS;YH;HFG;9SS;4H9GI".encode(self.FORMAT))

    def sendData(self, data):
        self.sock.send((f"{self.name}: " + data).encode(self.FORMAT))


if __name__ == "__main__":
    c = client()