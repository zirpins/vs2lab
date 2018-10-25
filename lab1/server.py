import socket

import constCS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((constCS.HOST, constCS.PORT))
s.listen(1)

(connection, address) = s.accept()  # returns new socket and address of client

while True:  # forever
    data = connection.recv(1024)  # receive data from client
    if not data:
        break  # stop if client stopped
    connection.send(data + "*".encode('utf-8'))  # return sent data plus an "*"

connection.close()  # close the connection
