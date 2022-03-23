import socket
import threading

SEND_IP = "192.168.1.69"
RECEIVE_IP = socket.gethostbyname(socket.gethostname())
print(RECEIVE_IP)
UDP_PORT = 8080


def listen_to_RIO():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RECEIVE_IP, UDP_PORT))
    msg = ""
    while(True):
        data, addr = sock.recvfrom(2048)
        print("data: " + data)
        print("addr: " + addr)
        msg = data
        if(msg == "GET"):
            break


def send_to_RIO(message: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(message), (SEND_IP, UDP_PORT))
    print("sending data: " + bytes(message))


def __main__():
    listenThread = threading.Thread(target=listen_to_RIO)
    sendThread = threading.Thread(target=send_to_RIO, args=["hi from nano"])
    listenThread.start()
    sendThread.start()
    print("done")
