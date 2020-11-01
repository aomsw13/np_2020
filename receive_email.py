import sys
from socket import * 
from tkinter import*
import tkinter
from tkinter import Menu
from tkinter import filedialog


def receive():
    serverPort = 8080
    message = [' ']
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect(('192.168.1.40', serverPort))
        # default text to send to server
    # or server from cmd line arg 1
    # or text from cmd line args 2..n # one message for each arg listed
    # make a TCP/IP socket object
    # connect to server machine and port
    for line in message: 
        sockobj.send(line.encode('utf-8'))
        data = sockobj.recv(1024)
    Info_receive = Label(frame,text = data.decode('utf-8'))
    Info_receive.pack()
    # print ('Client received:', data.decode('utf-8'))
        

    sockobj.close()

window = Tk()
window.title("Receive")
window.geometry("430x550")
frame=Frame(window)
frame.pack()
text_receive = Label(frame, text = 'Receive')
text_receive.pack()
Button1=Button(frame,text="Receive",fg='red', command = receive)
Button1.pack()
window.mainloop()