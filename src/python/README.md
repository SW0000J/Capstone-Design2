# Source Code Description

-------------------------

## Requirements

- ```python 3.9```
- ```msgpack 0.6.2```

## Installation

```
# Install python's message pack
pip3 install msgpack
```

## Run

```
# Run core
python3 Core.py

# Run edge
python3 Edge.py

# Run client
python3 Client.py

# Open Server.log
vi Server.log
```

## Core.py

```StartCore()```를 통한 Socket 스레드 할당

```python
def StartCore(self):
    ...

    edgeThread = threading.Thread(target=self.ConnectEdge, args=(edgeSock, )).start()
    clientThread = threading.Thread(target=self.ConnectClient, args=(clientSock, )).start()
```

```SyncEdge()```를 통한 데이터 동기화 로직

⚠️데이터 동기화 알고리즘 개선 필요⚠️

```python
def SyncEdge(self, socket):
    while True:
        request = socket.recv(1024)
        request = Packet(request)

        for edgeSock, edgeAdd in self.mEdgeList:
            if edgeSock != socket:
                edgeSock.send(request.GetData())
```

### Load Balancing

```GetResponse()```를 통해 Edge의 응답시간과 Edge에 붙어있는 클라이언트 개수 확인

```python
def GetResponse(self):
    ... 

        for edgeSock, edgeAdd in self.mEdgeList:
            tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmpSock.connect((...))

            startTime = time.time()

            tmpSock.send(...)
            response = tmpSock.recv(1024)
            clientCountList.append(int(response))

            responseTime = time.time()-startTime
            responseList.append(responseTime)
    ...
        return responseList, clientCountList
```

```GetResponse()```를 통해 얻은 응답시간 결과나 클라이언트 개수를 활용해 각 로드밸런싱 알고리즘에 적용

```python
def RandomLoadBalancer(self):
    ...
    
def RRLoadBalancer(self):
    ...
    
def BestResponseLoadBalancer(self):
    ...

def LeastConnectLoadBalancer(self):
    ...
```

## Edge.py

Edge는 각 클라이언트에서의 연산을 분산해 담당

```ToCore```, ```ToClient()```는 데이터 주고받는 함수

Client -> Core로의 데이터 전송과 Core -> Client로의 전송을 담당

⚠️데이터 동기화 알고리즘 개선 필요⚠️

```python
def ToCore(self, coreSocket, clientSocket):
    while True:
        request = Packet(clientSocket.recv(1024))
        coreSocket.send(request.GetData())
        
        ...

def ToClient(self, coreSocket):
        while True:
            request = Packet(coreSocket.recv(1024))
            
            for cliSock, cliAdd in self.mClientList:
                    cliSock.send(request.GetData())
                    ...
```

## Client.py

Client는 1초에 10번 Edge에 데이터를 전송하도록 함

```python
def SendEdge(self, socket):
        while True:
            time.sleep(0.1)

            msg = Packet()
            socket.send(msg.GetData())
    

def ReceiveEdge(self, socket):
    while True:
        request = socket.recv(1024)
```