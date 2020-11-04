import sys, os
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
    Info_receive = Label(text = data.decode('utf-8'), anchor='n' ,justify='left')
    Info_receive.pack()

    # print ('Client received:', data.decode('utf-8'))
        
    sockobj.close()
    # a = Label(text = '---------------------------------------------------- ')
    # a.pack()

def open_inbox():
    text = Label(text = '------------------------ Email From Inbox --------------------------- \n')
    text.pack()
    
    file1 = filedialog.askopenfile()
    filename = os.path.basename(str(file1.name))
    path = 'inbox/'
    filename = os.path.join(path, filename) 
    f = open(filename,'r',encoding='utf8')
    info_email = f.read()
    Last_email = Label(text = info_email, anchor='n' ,justify='left')
    Last_email.pack()
    f.close()

window = Tk()
window.title("Receive")
window.geometry("430x550")

text_receive = Label(window, text = 'Receive')
text_receive.pack(padx=30,pady=10)
Button1=Button(window,text="Receive",fg='red', command = receive)
Button1.pack(padx=10)
Button2=Button(window,text="Open Inbox",fg='blue', command = open_inbox)
Button2.pack(padx=10)
window.mainloop()