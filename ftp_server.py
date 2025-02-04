# this is a ftp server waiting a client to connect
import socket
import sys
import time
import os
import struct

print("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

# Initialise socket stuff
TCP_IP = "10.98.4.146" # Only a local server
TCP_PORT = 8000 # Just a random choice
BUFFER_SIZE = 1024 # Standard size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


def upld():
    # Send message once server is ready to recieve file details
    print('server is ready for client to upload')
    conn.send("server send ok 1".encode())
    # Recieve file name length, then file name
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size)
    # Send message to let client know server is ready for document content
    conn.send("server send ok 2".encode())
    # Recieve file size
    file_size = struct.unpack("i", conn.recv(4))[0]
    # Initialise and enter loop to recive file content
    start_time = time.time()
    output_file = open('testimg_output.jpg', "wb")
    # This keeps track of how many bytes we have recieved, so we know when to stop the loop
    bytes_recieved = 0
    print("\nRecieving...")
    while bytes_recieved < file_size:
        l = conn.recv(BUFFER_SIZE)
        if not l:
            break
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print("\nRecieved file: {}".format(file_name))
    # Send upload performance details
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    conn.close()
    return

def dwld():
    conn.send("server send ok 1".encode())
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    print('heelo server')
    print(file_name_length)
    file_name = conn.recv(file_name_length)
    print(file_name.decode())
    if os.path.isfile(file_name):
        # Then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        # Then the file doesn't exist, and send error code
        print("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    # Wait for ok to send file
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    start_time = time.time()
    print("Sending file...")
    content = open(file_name, "rb")
    # Again, break into chunks defined by BUFFER_SIZE
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return


while True:
    # Enter into a while loop to recieve commands from client
    conn, addr = s.accept()

    print("\nConnected to by address: {}".format(addr))

    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE)
    print("\nRecieved instruction: {}".format(data))
    # Check the command and respond correctly
    if data.decode() == "UPLD":
        upld()
    elif data == "LIST":
        list_files()
    elif data.decode() == "DWLD":
        dwld()