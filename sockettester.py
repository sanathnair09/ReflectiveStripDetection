import socket

UDP_IP = "localhost"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
info = (UDP_IP, UDP_PORT)
sock.bind(info)
data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
print("received message: %s" % data)
