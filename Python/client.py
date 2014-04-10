# Echo client program
import socket

HOST = 'localhost'
PORT = 50008
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while 1:
	data = s.recv(6000)
	print ': ', repr(data)

s.close()
