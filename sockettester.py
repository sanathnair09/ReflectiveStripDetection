import socket

SEND_IP = "192.168.86.27"
RECEIVE_IP = "172.17.0.1"
UDP_PORT = 8080
message = b"hello world"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((RECEIVE_IP, UDP_PORT))

# while(True):
#     data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     print("received message: %s" % data)


sock.sendto(message, (SEND_IP, UDP_PORT))
