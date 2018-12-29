import socket, sys, string, getpass

## To create Socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to connect")
    sys.exit();

print("[CLIENT]Socket Created")

## To declare the host and port
host = "localhost"
port = 25000

## Function to connect
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("[CLIENT]Hostname could not be resolved")
    sys.exit();

print("[CLIENT]IP Address: " + remote_ip)

s.connect((remote_ip, port))

print("[CLIENT]Socket Connected to " + host + " using IP " + remote_ip + "\n")

## Authorisation to connect to the server
authU = input("Username: ")
s.send(authU.encode())

authP = getpass.getpass()
s.send(authP.encode())

## Function to receive msg from server
rcvMsg = s.recv(4096)
rcvMsg = rcvMsg.decode()

if rcvMsg == "Wrong Username/Password!":
    rcvMsg = "\n<Server>" + rcvMsg + "\n"
    print(rcvMsg)
    sys.exit()
    
while True:
    fMsg = s.recv(4096)
    print("\n<Server>" + fMsg.decode() + "\n")
    
    ## Function to send msg to server
    message = input("<Client>")

    try:
        s.send(message.encode())
    except socket.error:
        print("[CLIENT]Did not send successfully")
        sys.exit()

    if message == "exit":
        print("Connection Lost")
        exit(0)

    if message == "<Client> red on" or message == "<Client> blue on" or message == "<Client> green on":    
        fMsg = s.recv(4096)
        print("\n<Server>" + fMsg.decode() + "\n")

        try:
            s.send(message.encode())
        except socket.error:
            print("[CLIENT]Did not send successfully")
            sys.exit()

        if message == "exit":
            print("Connection Lost")
            exit(0)
    
## To close socket
s.close()
