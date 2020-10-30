# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# This is a ftp client to UPLOAD and DOWNLOAD file to ftp server
from tkinter import *
from tkinter import ttk, filedialog
import os, sys
import tkinter as tk

import socket
import struct

BUFFER_SIZE = 1024  # Standard chioce

# create connection fro ftp client
def conn(file):
    # Initialise socket stuff
    TCP_IP = "10.98.4.36"  # Only a local server
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

    label_file = Label(window, text=filename, font=("Arial Bold", 10))
    label_file.grid(column=1, row=3)

    # define new text (you can modify this to your needs!)
    new_text = str(filename)
    # delete content from position 0 to end
    input_entry.delete(0, tk.END)
    # insert new_text at position 0
    input_entry.insert(0, new_text)

    upload_status = conn(filename) # create connection to ftp server

    print(upload_status)

    lable_success = Label(window, text=upload_status, font=("Arial Bold", 15))
    lable_success.grid(column=2, row=4)

def clicked_DNS():
    lable = Label(window, text="Welcome to DNS", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)


# redirect a user to ftp page after click a ftp button
def clicked_FTP():

    lable = Label(window, text="Welcome to FTP", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)

    entry_text = tk.StringVar()
    the_input = ttk.Entry(window, textvariable=entry_text)
    the_input.grid(column=1, row=2)

    # UPLOAD button
    upload_FTP = Button(window, text="UPLOAD", command=lambda: uploadFile(the_input), width=10, height=2)
    upload_FTP.grid(column=2, row=2)

    # DOWNLOAD button
    download_FTP = Button(window, text="DOWNLOAD", width=10, height=2)
    download_FTP.grid(column=4, row=2)


def clicked_Email():
    lable = Label(window, text="Welcome to Email", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)


def clicked_Web():
    lable = Label(window, text="Welcome to Web", font=("Arial Bold", 20))
    lable.grid(column=1, row=0)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()

    window.title("Welcome to ITCS428 Project")

    window.geometry('750x450')

    lbl = Label(window, text="Menu", font=("Arial Bold", 20), bg="grey", width=7, height=2)
    lbl.grid(column=0, row=0)

    btn_DNS = Button(window, text="DNS", command=clicked_DNS, width=10, height=2)
    btn_DNS.grid(column=0, row=1)

    btn_FTP = Button(window, text="FTP", command=clicked_FTP, width=10, height=2)
    btn_FTP.grid(column=0, row=2)

    btn_Email = Button(window, text="Email", command=clicked_Email, width=10, height=2)
    btn_Email.grid(column=0, row=3)

    btn_Web = Button(window, text="Web", command=clicked_Web, width=10, height=2)
    btn_Web.grid(column=0, row=4)


    window.mainloop()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
