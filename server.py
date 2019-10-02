import socket
from threading import Thread
import os.path

BUFF_SIZE=1024

#list of current clients
clients = []

class Client(Thread):
    #creation of client thread
    def __init__(self, name: str, sock: socket.socket):
        #add socket and name
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    def run(self):
        filename = self.sock.recv(BUFF_SIZE).decode()
        ind = 1
        #check file name
        if os.path.isfile(filename):
            while True:
                #find, where enter extension near nedded index
                index = filename.rindex('.')
                if os.path.isfile(filename[:index] + '(' + str(ind) + ')' + filename[index:]):
                    ind +=1
                else:
                    filename = filename[:index] + '(' + str(ind) + ')' + filename[index:]
                    break
        # write data from the file
        with open(filename, 'wb') as f:
            message = 'file created'
            self.sock.send(message.encode())
            while True:
                data = self.sock.recv(BUFF_SIZE)
                if data:
                    f.write(data)
                else:
                    self._close()
                    return

    #redefine close operation
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')


def main():
    next = 1
    #open socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()
    # add clients
    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'client' + str(next)
        next += 1
        print(str(addr) + ' connected, named as ' + name)
        Client(name, con).start()


if __name__ == "__main__":
    main()