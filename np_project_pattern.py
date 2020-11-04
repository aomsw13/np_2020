# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# For GUI Part
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox

# For DNS Part
import dns as dns
import dns.resolver
import dns.reversename
import socketserver, socket

# For FTP Part
import os, time, struct, sys

# Email Part
from email.parser import BytesParser, Parser
from email.policy import default

# HTTP Part
from html.parser import HTMLParser
from xml.etree import ElementTree


def searchDns():
    label_web.configure(text="DNS : ")
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

# FTP: Initialise socket stuff
TCP_IP = "10.62.16.47"  # Only a local server
TCP_PORT = 8000  # Just a random choice
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUFFER_SIZE = 1024  # Standard choice


# FTP: create connection between ftp client and ftp server
def conn():
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection successful")
        # temp_status = upload_server(file,s)
    except:
        print("Connection unsuccessful. Make sure the server is online.")
    # return temp_status


# FTP: open dialog file from computer
def openDialogFile(input_entry):
    # initaildir="<Your Server Path>"
    file1 = filedialog.askopenfile(initialdir="/Users/supakarn/PycharmProjects/np_2020")
    filename = os.path.basename(str(file1.name))

    label_file = Label(ftpTab, text=filename, font=("Arial Bold", 10))
    label_file.grid(column=1, row=3)

    # define new text (you can modify this to your needs!)
    new_text = str(filename)
    # delete content from position 0 to end
    input_entry.delete(0, tk.END)
    # insert new_text at position 0
    input_entry.insert(0, new_text)

    return filename


# FTP: start sending a file to server from client
def upload_server(file_name):
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


# FTP: open file dialog to allow a user select file to upload
def listUploadFile(input_entry):
    # open file dialog
    selected_file = openDialogFile(input_entry)
    # create connection to ftp server first
    conn()
    # return status whether client can upload file to server or not
    upload_status = upload_server(selected_file)

    print(upload_status)

    label_success = Label(ftpTab, text=upload_status, font=("Arial Bold", 15))
    label_success.grid(column=1, row=7)
    messagebox.showinfo("Upload Success!", upload_status)


# FTP: list all files from server to client for download
def listDownloadFile(input_entry):
    # open file dialog
    selected_file = openDialogFile(input_entry)
    # create connection to ftp server first
    conn()

    download_status = download_server(selected_file)

    label_success = Label(ftpTab, text=download_status, font=("Arial Bold", 15))
    label_success.grid(column=1, row=7)
    messagebox.showinfo("Download Success!", download_status)


# FTP: start download file from server to client
def download_server(file_name):
    # Download given file
    print("Downloading file: {}".format(file_name))
    try:
        # Send server request
        s.send("DWLD".encode())
    except:
        print("Couldn't make server request. Make sure a connection has bene established.")
        return
    try:
        print('ready to receive')
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            # If file size is -1, the file does not exist
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        # Send ok to receive file content
        s.send("1".encode())
        # Enter loop to receive file
        output_file = open('out' + file_name, "wb")
        bytes_received = 0
        print("\nDownloading...")
        while bytes_received < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_received += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        # Tell the server that the client is ready to receive the download performance details
        s.send("1".encode())
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except:
        print("Error downloading file")
        return "client can not download file"
    return "Success to download file from server"


def sending(from_add, to_add, subject, message):
    myHost = '10.62.16.47'
    myPort = 8080
    sockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockObj.bind((myHost, myPort))
    sockObj.listen(5)
    headers = Parser(policy=default).parsestr(
        'From: ' + from_add + '\n '
                              'To:' + to_add + '\n'
                                               'Subject:' + subject + '\n'
                                                                      '\n'
        + message + '\n')
    print(headers)
    while True:
        connection, address = sockObj.accept()
        print('Server connected by', address)
        while 1:
            data = connection.recv(1024)
            if not data: break
            message = str(headers).encode('utf-8') + data
            connection.send(message)
    connection.close()


def uri_split(uri, sender_email):
    # URI Split for Email
    uri_all = uri.get().split(":", 1)
    if uri_all[0] == 'mailto':
        mail_split = uri_all[1].split("?subject=", 1)
        mail = mail_split[0]
        subject_split = mail_split[1].split("&body=", 1)
        subject = subject_split[0]
        body = subject_split[1]
        sending(sender_email.get(), mail, subject, body)

    elif uri_all[0] == 'ftp':
        print(uri_all[1])
        ftp_split = uri_all[1].split("//", 1)
        ip_split = ftp_split[1].split(":", 1)
        ip = ip_split[0]
        port_split = ip_split[1].split("/", 2)
        port = port_split[0]
        path = port_split[1]
        filename = port_split[2]

    elif uri_all[0] == 'http' or uri_all[0] == 'https':
        url_split = uri_all[1].split("//", 1)
        url_link = url_split[1]
        print(url_split[1])


if __name__ == '__main__':
    window = Tk()

    window.title("Welcome to ITCS428 Project")
    window.geometry('12000x700')

    tabControl = ttk.Notebook(window, height=100)

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
    label_web = Label(dnsTab, text="DNS : ")
    label_web.pack()
    label_web.grid(column=0, row=0)
    inputDns = Entry(dnsTab, width=50)
    inputDns.grid(column=1, row=0)

    btnDns = Button(dnsTab, text="Search", command=searchDns)
    btnDns.grid(column=2, row=0)

    # FTP Tab
    label_web = Label(ftpTab, text="Select File ")
    label_web.pack()
    label_web.grid(column=0, row=0)
    inputFtp = Entry(ftpTab, width=45)
    inputFtp.grid(column=1, row=0)

    btnFtp_upload = Button(ftpTab, text="Upload", command=lambda: listUploadFile(inputFtp))
    btnFtp_upload.grid(column=2, row=0)

    btnFtp_download = Button(ftpTab, text="Download", command=lambda: listDownloadFile(inputFtp))
    btnFtp_download.grid(column=3, row=0)

    # Email Tab
    label_web = Label(emailTab, text="From ")
    label_web.pack()
    label_web.grid(column=0, row=1)
    inputFrom = Entry(emailTab, width=50)
    inputFrom.grid(column=1, row=1)

    label_web = Label(emailTab, text="To ")
    label_web.grid(column=0, row=2)
    inputTo = Entry(emailTab, width=50)
    inputTo.grid(column=1, row=2)

    label_web = Label(emailTab, text="Subject ")
    label_web.grid(column=0, row=3)
    inputSubject = Entry(emailTab, width=50)
    inputSubject.grid(column=1, row=3)

    label_web = Label(emailTab, text="Message ")
    label_web.grid(column=0, row=4)
    message_body = Text(emailTab, width=65, height=10)
    message_body.grid(column=1, row=4)

    btnFtp_upload = Button(emailTab, text="Send",
                           command=lambda: sending(inputFrom.get(), inputTo.get(), inputSubject.get(),
                                                   message_body.get('1.0', END)))
    btnFtp_upload.grid(column=1, row=5)

    # Web Client Tab
    label_web = Label(webTab, text="URI : ")
    label_web.pack()
    label_web.grid(column=0, row=0)
    inputWeb = Entry(webTab, width=50)
    inputWeb.grid(column=1, row=0)

    label_web = Label(webTab, text="Sender Email : ")
    label_web.grid(column=0, row=1)
    inputSender = Entry(webTab, width=50)
    inputSender.grid(column=1, row=1)

    btnWeb = Button(webTab, text="Enter", command=lambda: uri_split(inputWeb, inputSender))
    btnWeb.grid(column=2, row=0)

    window.mainloop()
