import threading
import socket

from Logger import Logger
from Packet import Packet


class Edge:
    def __init__(self, ip, corePort=6679, clientPort=6680):
        self.mIP = ip
        self.mCorePort = corePort
        self.mClientPort = clientPort

        self.mClientList = []
        self.mClientCount = 0

        self.mLog = Logger("EdgeLog", "Server.log")

        self.StartEdge()

    
    def StartEdge(self):
        # Initialize core socket
        coreSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        coreSock.connect((self.mIP, self.mCorePort))

        # Set edge's client port
        self.mClientPort = int(coreSock.recv(1024))
        print(self.mClientPort)

        # Initialize client socket
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSock.bind((self.mIP, self.mClientPort))
        clientSock.listen(5)

        tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmpSock.bind((self.mIP, self.mClientPort+200))
        tmpSock.listen(5)

        sendThread = threading.Thread(target=self.ConnectSocket, args=(coreSock, clientSock, )).start()
        responseThread = threading.Thread(target=self.ResponseCore, args=(tmpSock, )).start()

    
    def ConnectSocket(self, coreSocket,  clientSocket):
        while True:
            cliSock, address = clientSocket.accept()

            self.mLog.PrintLog("***Client Connection***")
            self.mLog.PrintLog(f"Total Client: {self.mClientCount+1}")
            print(self.mClientCount)
            self.mClientList.append((cliSock, address))
            self.mClientCount += 1
            
            coreHandler = threading.Thread(target=self.ToCore, args=(coreSocket, cliSock, )).start()
            clientHandler = threading.Thread(target=self.ToClient, args=(coreSocket, )).start()


    def ToCore(self, coreSocket, clientSocket):
        while True:
            request = Packet(clientSocket.recv(1024))
            coreSocket.send(request.GetData())
            self.mLog.PrintLog(f"Edge send to Core {request}")

    
    def ToClient(self, coreSocket):
        while True:
            request = Packet(coreSocket.recv(1024))
            
            for cliSock, cliAdd in self.mClientList:
                    cliSock.send(request.GetData())
                    self.mLog.PrintLog(f"Edge send to Client: {request}")

    
    def ResponseCore(self, tmpSocket):
        while True:
            tmpSock, address = tmpSocket.accept()
            
            response = tmpSock.recv(1024)

            tmpSock.send(bytes(str(self.mClientCount), "utf8"))
            self.mLog.PrintLog("Edge response to Core!")
            print("Response:", address)

            #tmpSock.close()


if __name__ == "__main__":
    print("Edge")
    edge = Edge("127.0.0.1")