import socket
import os.path
import sys

BUFF_SIZE = 1024

def main():
    # write input data
    filename = str(sys.argv[1])
    port = int(sys.argv[3])
    host = str(sys.argv[2])
    sock = socket.socket()
    # open socket connection
    sock.connect((host, port))
    sock.send(filename.encode())
    f = open(str(filename), 'rb')
    size = os.path.getsize(filename)
    bytes_transported = BUFF_SIZE
    read = f.read(BUFF_SIZE)
    print(sock.recv(BUFF_SIZE).decode())

    # while there is something to read
    while read:
        print("Finished {0} %".format(bytes_transported * 100 // size))
        bytes_transported += BUFF_SIZE
        sock.send(read)
        read = f.read(BUFF_SIZE)
    # close connection
    sock.close()
    f.close()
    print('Download finished')


if __name__ == "__main__":
    main()
