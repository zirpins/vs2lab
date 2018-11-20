# ZeroMQ

## Nachrichtenbasiertes Datenodell

- ZeroMQ basiert auf Nachrichtenübertragung, nicht Streams
- Server braucht keine Größe empfangener Daten

## Request Reply Pattern

- Socket hört auf mehreren Ports

```
p1 = "tcp://" + HOST + ":" + PORT1  # how and where to connect
p2 = "tcp://" + HOST + ":" + PORT2  # how and where to connect

context = zmq.Context()
s = context.socket(zmq.REP)  # create reply socket

s.bind(p1)  # bind socket to address
s.bind(p2)  # bind socket to address
```

- Reply Nachricht geht immer an zugehörige Request Adresse

```
while True:
    message = s.recv()  # wait for incoming message
    s.send((message.decode() + "*").encode()) 
```

## Asynchrones Verhalten

- Client blockiert bis Server bereit ist

1. starte client
2. starte server


1. Starte Server
2. Starte Client1 (Server stoppt)
3. Starte Client2
4. Starte Server