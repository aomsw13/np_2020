# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# For GUI Part
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, Menu
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

# For DNS Part
import argparse
import dns as dns
import dns.resolver
import dns.reversename
import socketserver, socket
from socket import AF_INET, SOCK_STREAM

# For FTP Part
import os, time, struct, sys

# Email Part
from email.parser import BytesParser, Parser
from email.policy import default

def searchDns():
    lable.configure(text="DNS : ")
    # IPv4 Records
    ipv4 = dns.resolver.resolve(inputDns.get(), 'A')
    title_ipv4 = ttk.Label(text='IPv4 Record for %s is: ' % inputDns.get())
    title_ipv4.pack()
    for data in ipv4:
        output_ipv4 = ttk.Label(text=data.to_text())
        output_ipv4.pack()

    # IPv6 Records
    ipv6 = dns.resolver.resolve(inputDns.get(), 'AAAA')
    title_ipv6 = ttk.Label(text='IPv6 Record for %s is: ' % inputDns.get())
    title_ipv6.pack()
    for data in ipv6:
        output_ipv6 = ttk.Label(text=data.to_text())
        output_ipv6.pack()

    # MX Records
    mail = dns.resolver.resolve(inputDns.get(), 'MX')
    title_MX = ttk.Label(text='MX Record for %s is: ' % inputDns.get())
    title_MX.pack()
    for data in mail:
        output_mail = ttk.Label(text=data.exchange.to_text())
        output_mail.pack()

    # NS Records
    name = dns.resolver.resolve(inputDns.get(), 'NS')
    title_NS = ttk.Label(text='NS Record for %s is: ' % inputDns.get())
    title_NS.pack()
    for data in name:
        output_name = ttk.Label(text=data.to_text())
        output_name.pack()
        
    # Find FQDN 
    title_fqdn = ttk.Label(text='FQDN for %s is: ' % inputDns.get())
    title_fqdn.pack()
    fqdn_result = socket.getfqdn(inputDns.get())
    output_fqdn = ttk.Label(text=fqdn_result)
    output_fqdn.pack()


def now():
    return time.ctime(time.time())

BUFFER_SIZE = 1024

# create connection for ftp client
def conn(file, status):
    # Initialise socket stuff
    TCP_IP = "192.168.1.40"  # Only a local server
    TCP_PORT = 8000  # Just a random choice
    # BUFFER_SIZE = 1024  # Standard chioce
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection sucessful")
        if(status == 'upload'):
            temp_status = upload_server(file,s)
        #elif(status == 'download'):
            #temp_status = download_(file)
    except:
        print("Connection unsucessful. Make sure the server is online.")
    return temp_status

def upload_server(file_name,s):
    # Upload a file
    file_name = file_name.encode()
    print("\nUploading file: {}...".format(file_name))
    try:
        # Check the file exists
        print("filename: ", file_name)
        content = open(file_name, "rb")
    except:
        print("Couldn't open file. Make sure the file name was entered correctly.")
        return
    try:
        # Make upload request
        s.send("UPLD".encode())
    except:
        print("Couldn't make server request. Make sure a connection has bene established.")
        return
    try:
        # Wait for server acknowledgement then send file details
        # Wait for server ok
        data1 = s.recv(BUFFER_SIZE)
        print("recv from server ", data1)
        # Send file name size and file name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name)
        # Wait for server ok then send file size
        data2 = s.recv(BUFFER_SIZE)
        print("recv from server ", data2)
        s.send(struct.pack("i", os.path.getsize(file_name)))

        print("Success to send file details")

    except:
        print("Error sending file details")
    try:
        # Send the file in chunks defined by BUFFER_SIZE
        # Doing it this way allows for unlimited potential file sizes to be sent
        l = content.read(BUFFER_SIZE)
        print("\nSending...")
        while l:
            s.sendall(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        # Get upload performance details
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
        s.close()

    except:
        print("Error sending file")
        return "Cannot upload file to server"
    return "Success to upload file to server"

# open file dialog to allow a user select file to upload
def uploadFile(input_entry):

    # file = open("users.txt", "w")
    # user_Input = text_File.get()
    # file.write(user_Input)
    # file.close()

    file1 = filedialog.askopenfile()
    filename = os.path.basename(str(file1.name))

    label_file = Label(ftpTab, text=filename, font=("Arial Bold", 10))
    label_file.grid(column=1, row=3)

    # define new text (you can modify this to your needs!)
    new_text = str(filename)
    # delete content from position 0 to end
    input_entry.delete(0, tk.END)
    # insert new_text at position 0
    input_entry.insert(0, new_text)

    upload_status = conn(filename,'upload') # create connection to ftp server

    print(upload_status)

    lable_success = Label(ftpTab, text=upload_status)
    lable_success.grid(column=1, row=4)  
    messagebox.showinfo("Upload Success!", upload_status)   

def sending (from_add, to_add, subject, message):
       
    myHost = '192.168.1.40'
    myPort = 8080
    sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sockobj.bind((myHost, myPort)) 
    sockobj.listen(5)
    headers = Parser(policy=default).parsestr(
            'From: ' + from_add.get() +'\n '
            'To:'+ to_add.get()+'\n'
            'Subject:'+ subject.get() +'\n'
            '\n'
            +(message.get('1.0',END))+'\n')
    print(headers)
    while True:
        connection, address = sockobj.accept() 
        print ('Server connected by', address)
        while 1:
            data = connection.recv(1024)
            if not data: break
            message = str(headers).encode('utf-8') + data
            connection.send(message)
    connection.close()

if __name__ == '__main__':
    
    window = Tk()

    window.title("Welcome to ITCS428 Project")
    window.geometry('750x450')

    tabControl = ttk.Notebook(window)

    dnsTab = ttk.Frame(tabControl)
    ftpTab = ttk.Frame(tabControl)
    emailTab = ttk.Frame(tabControl)
    webTab = ttk.Frame(tabControl)

    tabControl.add(dnsTab, text='DNS')
    tabControl.add(ftpTab, text='FTP')
    tabControl.add(emailTab, text='Email')
    tabControl.add(webTab, text='Web')
    tabControl.pack(expand=1, fill="both")

    # DNS Tab

    lable = Label(dnsTab, text="DNS : ")
    lable.pack()
    lable.grid(column=0, row=0)
    inputDns = Entry(dnsTab, width=50)
    inputDns.grid(column=1, row=0)

    btnDns = Button(dnsTab, text="Search", command=searchDns)
    btnDns.grid(column=2, row=0)

    # FTP Tab
    lable = Label(ftpTab, text="Select File ")
    lable.pack()
    lable.grid(column=0, row=0)
    inputFtp = Entry(ftpTab, width=45)
    inputFtp.grid(column=1, row=0)

    btnFtp_upload = Button(ftpTab, text="Upload", command=lambda: uploadFile(inputFtp))
    btnFtp_upload.grid(column=2, row=0)

    btnFtp_download = Button(ftpTab, text="Download", command=lambda: '')
    btnFtp_download.grid(column=3, row=0)

    # Email Tab
    lable = Label(emailTab, text="From ")
    lable.pack()
    lable.grid(column=0, row=1)
    inputFrom = Entry(emailTab, width=50)
    inputFrom.grid(column=1, row=1)

    lable = Label(emailTab, text="To ")
    lable.grid(column=0, row=2)
    inputTo = Entry(emailTab, width=50)
    inputTo.grid(column=1, row=2)

    lable = Label(emailTab, text="Subject ")
    lable.grid(column=0, row=3)
    inputSubject = Entry(emailTab, width=50)
    inputSubject.grid(column=1, row=3)

    lable = Label(emailTab, text="Message ")
    lable.grid(column=0, row=4)
    message_body = Text(emailTab, width=65, height=10)
    message_body.grid(column=1, row=4)

    btnFtp_upload = Button(emailTab, text="Send", command=lambda: sending(inputFrom, inputTo, inputSubject, message_body))
    btnFtp_upload.grid(column=1, row=5)

    # ttk.Label(dnsTab,
    #           text="Welcome to \
    # GeeksForGeeks").grid(column=0,
    #                      row=0,
    #                      padx=30,
    #                      pady=30)

    window.mainloop()
