import socket, sys, time, datetime
from _thread import *
import RPi.GPIO as GPIO
import time
    
## Define Pin on Raspberry Pi
rPin = 27
bPin = 22
gPin = 17

## Function to turn on pin
def turnOn(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

## Function to turn off pin
def turnOff(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW) 

def redOn():
    turnOn(rPin)
    
def greenOn():
    turnOn(gPin)

def blueOn():
    turnOn(bPin)

def redOff():
    turnOff(rPin)

def greenOff():
    turnOff(gPin)
    
def blueOff():
    turnOff(bPin)

def blink(color, uTime):
    t_end = time.time() + int(uTime)
    
    while time.time() < t_end:
        turnOn(color)
        time.sleep(0.5)
        turnOff(color)
        time.sleep(0.5) 
    

########################################################
    
## Host '' means that we enable any host to enter
host = ''
port = 25000

## Create Socket Function
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("[SERVER]Socket Created")

## To bind Function
try:
    s.bind((host,port))
except socket.error:
    print("[SERVER]Binding Failed")
    sys.exit()

print("[SERVER]Socket has been binded")

## To listen function, 10 mean up to 10 people able to queue to handle a request
s.listen(10)

print("[SERVER]Socket Is Ready\n")

## Function for multi client
def clientthread(conn):
    ## Authorisation

    ## Get username from user
    data = conn.recv(1024)
    authU = data.decode()

    ## Get password from user
    data = conn.recv(1024)
    authP = data.decode()

    if authU == "hanif" and authP == "123":
        lCheck = True

        ## Function to send    
        welcomemsg = "-----Raspberry Pi RGB LED Controller-----"
        conn.send(welcomemsg.encode())
        
        while lCheck:

            fMsg = "color on/off"
            conn.send(fMsg.encode())

            ##Function to receive
            data = conn.recv(4096)
            if not data:
                break;
      
            reply = "<Client>" + data.decode()
            print(reply)
            uInput = data.decode()
            uInput2 = ""
            
            if uInput == "red on" or uInput == "blue on" or uInput == "green on":
                fMsg = "blink yes/no"
                conn.send(fMsg.encode())

                data = conn.recv(4096)
                reply = "<Client>" + data.decode()
                print(reply)

                uInput2 = data.decode()
                
                if uInput2 == "blink yes":               
                    fMsg = "time"
                    conn.send(fMsg.encode())
                
                    data = conn.recv(4096)
                    reply = "<Client>" + data.decode()
                    print(reply)
                
                    uInput3 = data.decode()

            if uInput == "red on" and uInput2 == "blink yes":
                blink(rPin, uInput3)
            elif uInput == "blue on" and uInput2 == "blink yes":
                blink(bPin, uInput3)
            elif uInput == "green on" and uInput2 == "blink yes":
                blink(gPin, uInput3)
            elif uInput == "red on" and uInput2 == "blink no":
                redOn()
            elif uInput == "blue on" and uInput2 == "blink no":
                blueOn()
            elif uInput == "green on" and uInput2 == "blink no":
                greenOn()
            elif uInput == "red off":
                redOff()
            elif uInput == "blue off":
                blueOff()
            elif uInput == "green off":
                greenOff()
            elif uInput == "exit" or uInput2 == "exit":
                lCheck = False
            else:
                print("\nInvalid Command!")
                sMsg = "Invalid Command"
                conn.send(sMsg.encode())

        ## Out of while loop        
        print("Connection lost from " + addr[0] + ":" + str(addr[1]))
        conn.close()
        return
    else:
        print("Username/Password is Invalid!")
        authmsg = "Wrong Username/Password!"
        conn.send(authmsg.encode())
        conn.close()    

## Function to save connection into file
def saveFile(addr):
    f = open("conLog.txt", "a+")

    millis = int(round(time.time() * 1000))
    millis = str(millis)

    ## msg = "[CONNECTED] 192.168.10.3 on " + datetime.date.today().strftime("%A %d/%m/%Y") + " at " + datetime.datetime.now().strftime("%H:%M:%S:") + millis + "\n"
    msg = "[CONNECTED] " + addr[0] + ":" + str(addr[1]) + " on " + datetime.date.today().strftime("%A %d/%m/%Y") + " at " + datetime.datetime.now().strftime("%H:%M:%S:") + millis + "\n"
    f.write(msg)
    f.close

## Main function to loop the server   
while 1:
    ## To accept function
    conn, addr = s.accept()
    saveFile(addr)
    print("[SERVER]Connected with " + addr[0] + ":" + str(addr[1]) + "\n")
    start_new_thread(clientthread, (conn,))
    
s.close()
