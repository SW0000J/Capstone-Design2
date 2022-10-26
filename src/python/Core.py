import threading
import time
import socket
import random


class Core:
    def __init__(self, ip, edgePort, clientPort):
        self.mIP = ip
        self.mEdgePort = edgePort
        self.mClientPort = clientPort

        self.mEdgeList = []
        self.mEdgeCount = 0

        self.rrIndex = 0

        self.StartCore()

    
    def StartCore(self):
        # Initialize edge's socket
        edgeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        edgeSock.bind((socket.gethostname(), self.mEdgePort))
        edgeSock.listen(5)
        # Initialize client's socket
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSock.bind((socket.gethostname(), self.mClientPort))
        clientSock.listen(5)

        edgeThread = threading.Thread(target=self.ConnectEdge, args=(edgeSock, )).start()
        clientThread = threading.Thread(target=self.ConnectClient, args=(clientSock, )).start()

    
    def ConnectEdge(self, socket):
        while True:
            sock, address = socket.accept()
            
            print(self.mEdgeCount)
            self.mEdgeList.append((sock, address))
            self.mEdgeCount += 1

            # Make edge's client port
            sock.send(bytes(str(self.mEdgePort+self.mEdgeCount), "utf8"))

            syncEdgeHandler = threading.Thread(target=self.SyncEdge, args=(sock, )).start()

    
    def SyncEdge(self, socket):
        while True:
            request = socket.recv(1024)

            for edgeSock, edgeAdd in self.mEdgeList:
                if edgeSock != socket:
                    edgeSock.send(request)

    
    def ConnectClient(self, socket):
        while True:
            sock, address = socket.accept()
            print("Client {}".format(address))
            
            matchEdgeHandler = threading.Thread(target=self.MatchEdge, args=(sock, )).start()


    def MatchEdge(self, socket):
        edgePort = self.LeastConnectLoadBalancer()

        print(edgePort)
        socket.send(bytes(str(edgePort), 'utf8'))


    def RandomLoadBalancer(self):
        if self.mEdgeCount > 0:
            return random.randrange(6680, 6680+self.mEdgeCount)
        else:
            return -1

    
    def RRLoadBalancer(self):
        edgePort = 6680 + self.rrIndex
        self.rrIndex = (self.rrIndex + 1) % self.mEdgeCount

        return edgePort

    
    def BestResponseLoadBalancer(self):
        responseList, clientCountList = self.GetResponse()
        print(responseList)

        return 6680+responseList.index(min(responseList))

    
    def LeastConnectLoadBalancer(self):
        responseList, clientCountList = self.GetResponse()
        print(clientCountList)

        return 6680+clientCountList.index(min(clientCountList))

    
    def GetResponse(self):
        responseList = []
        clientCountList = []
        edgeCount = 1
        for edgeSock, edgeAdd in self.mEdgeList:
            print(self.mEdgePort+edgeCount+200)
            tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmpSock.connect((edgeAdd[0], self.mEdgePort+edgeCount+200))

            startTime = time.time()

            tmpSock.send(bytes("Core!", "utf8"))
            response = tmpSock.recv(1024)
            clientCountList.append(int(response))

            responseList.append(time.time()-startTime)
            edgeCount += 1

        return responseList, clientCountList



if __name__ == "__main__":
    print("Core")
    Core = Core("127.0.0.1", 6679, 6678)