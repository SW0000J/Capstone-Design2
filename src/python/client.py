import threading
import time
import socket


class Client:
    def __init__(self, ip, corePort=6678, edgePort=6680):
        self.mIP = ip
        self.mCorePort = corePort
        self.mEdgePort = edgePort

        self.StartClient()

    
    def StartClient(self):
        coreSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        coreSock.connect((self.mIP, self.mCorePort))

        self.mEdgePort = int(coreSock.recv(1024))
        coreSock.close()

        print(self.mEdgePort)

        edgeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.mIP, self.mEdgePort)
        edgeSock.connect((self.mIP, self.mEdgePort))

        sendThread = threading.Thread(target=self.SendEdge, args=(edgeSock, )).start()
        receiveThread = threading.Thread(target=self.ReceiveEdge, args=(edgeSock, )).start()

    
    def SendEdge(self, socket):
        while True:
            time.sleep(0.1)

            msg = 'a'*1024
            socket.send(bytes(msg, "utf8"))
    

    def ReceiveEdge(self, socket):
        while True:
            request = socket.recv(1024)


if __name__ == "__main__":
    print("Client")
    client = Client("127.0.0.1")