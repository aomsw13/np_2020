# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# For GUI Part
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

# For DNS Part
import argparse
import dns as dns
import dns.resolver
import dns.reversename
import socket, socketserver

# For FTP Part
import os, time, struct

def searchDns():
    lable.configure(text="DNS : ")
    # Find MX Record
    mail = dns.resolver.query(inputDns.get(), 'MX')
    title_MX = ttk.Label(text='MX Record for %s is: ' % inputDns.get())
    title_MX.pack()
    for data in mail:
        output_mail = ttk.Label(text=data.exchange.to_text())
        output_mail.pack()
        
    # Find FQDN 
    title_fqdn = ttk.Label(text='FQDN for %s is: ' % inputDns.get())
    title_fqdn.pack()
    fqdn_result = socket.getfqdn(inputDns.get())
    output_fqdn = ttk.Label(text=fqdn_result)
    output_fqdn.pack()


def now():
    return time.ctime(time.time())

BUFFER_SIZE = 1024

# create connection fro ftp client
def conn(file):
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
        temp_status = upload_server(file,s)
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

    upload_status = conn(filename) # create connection to ftp server

    print(upload_status)

    lable_success = Label(ftpTab, text=upload_status, font=("Arial Bold", 15))
    lable_success.grid(column=2, row=4)     


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
    inputFtp = Entry(ftpTab, width=50)
    inputFtp.grid(column=1, row=0)

    btnFtp = Button(ftpTab, text="Upload", command=lambda: uploadFile(inputFtp))
    btnFtp.grid(column=2, row=0)

    # ttk.Label(dnsTab,
    #           text="Welcome to \
    # GeeksForGeeks").grid(column=0,
    #                      row=0,
    #                      padx=30,
    #                      pady=30)

    window.mainloop()
