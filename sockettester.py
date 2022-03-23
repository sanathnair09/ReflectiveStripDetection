from random import Random
import socket
import threading

SEND_IP = "192.168.1.69"  # roborio IP
RECEIVE_IP = "192.168.1.18"  # nano IP
UDP_PORT = 8080  # port


def getAngleToTurn():
    angle = Random.randint(0, 120)
    return str(angle)


def listen_to_RIO():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RECEIVE_IP, UDP_PORT))
    msg = ""
    while(True):
        data, addr = sock.recvfrom(2048)
        print("data: " + data)
        print("addr: " + str(addr))
        msg = data
        if(msg == "GET"):
            # def get coords
            angle = getAngleToTurn()
            send_to_RIO(angle)


def send_to_RIO(message: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(message), (SEND_IP, UDP_PORT))
    print("sent data")


while(True):
    listen_to_RIO()
