from threading import Thread
import socket
import time
import sys
import RPi.GPIO as GPIO

IP_ADDRESS_SEND = "Enter IP address of System running Game"
IP_PORT_SEND = 22002

VERBOSE = True
IP_PORT = 22001
motor1a = 7
motor1b = 11
motor1e = 22

motor2a = 13
motor2b = 16
motor2e = 15

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motor1a,GPIO.OUT)
    GPIO.setup(motor1b,GPIO.OUT)
    GPIO.setup(motor1e,GPIO.OUT)
    GPIO.setup(motor2a,GPIO.OUT)
    GPIO.setup(motor2b,GPIO.OUT)
    GPIO.setup(motor2e,GPIO.OUT)

def debug(text):
    if VERBOSE:
        print "Debug:---", text
        
        # ---------------------- class SocketHandler -------Client-----------------
def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sockSend.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
        closeConnection()
        
        def closeConnection():
            global isConnected
    debug("Closing socket")
    sockSend.close()
    isConnected = False

def connect():
    global sockSend
    sockSend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockSend.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    debug("Connecting...")
    try:
        sockSend.connect((IP_ADDRESS_SEND, IP_PORT_SEND))
    except:
        debug("Connection failed.")
        return False
    return True

sockSend = None
isConnected = False
def sendData():
    if connect():
        isConnected = True
        print "Connection established"
        sendCommand("go")
 
    else:
        print "Connection to %s:%d failed" % (IP_ADDRESS_SEND, IP_PORT_SEND)
        print "done"  
        
# ---------------------- class SocketHandler -------Srvr-----------------
class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global isConnected
        debug("SocketHandler started")
        while True:
            cmd = ""
            try:
                debug("Calling blocking conn.recv()")
                cmd = self.conn.recv(1024)
            except:
                debug("exception in conn.recv()") 
                # happens when connection is reset from the peer
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if len(cmd) == 0:
                break
            self.executeCommand(cmd)
        conn.close()
        print "Client disconnected. Waiting for next client..."
        isConnected = False
        debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        debug("Calling executeCommand() with  cmd: " + cmd)
        if cmd == "up":  # remove trailing "\0"
                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor1e,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW)
                GPIO.output(motor1a,GPIO.LOW) #MOTOR1
                GPIO.output(motor2b,GPIO.LOW) #MOTOR2
                GPIO.output(motor1e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor2e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1b,GPIO.HIGH) #MOTOR2
                GPIO.output(motor2a,GPIO.HIGH) #MOTOR2
        elif cmd == "down":
                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor1e,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW) #MOTOR1
                GPIO.output(motor2a,GPIO.LOW) #MOTOR2
                GPIO.output(motor1e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1a,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1b,GPIO.HIGH) #MOTOR2
                GPIO.output(motor2b,GPIO.HIGH) #MOTOR2
        elif cmd == "right":
                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor1e,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW)
                GPIO.output(motor1e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor2e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1b,GPIO.HIGH) #MOTOR2
                GPIO.output(motor2b,GPIO.HIGH) #MOTOR2
        elif cmd == "left":
                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor1e,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW)
                GPIO.output(motor1e,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1a,GPIO.HIGH) #MOTOR1
                GPIO.output(motor1b,GPIO.HIGH) #MOTOR2
                GPIO.output(motor2a,GPIO.HIGH) #MOTOR2
        elif cmd == "brake":
                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor1e,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.LOW)
                GPIO.output(motor2e,GPIO.LOW)
# ----------------- End of SocketHandler -----------------------

setup()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# close port when process exits:
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
debug("Socket created")
HOSTNAME = "" # Symbolic name meaning all available interfaces
try:
    serverSocket.bind((HOSTNAME, IP_PORT))
except socket.error as msg:
    print "Bind failed", msg[0], msg[1]
    sys.exit()
serverSocket.listen(10)

print "Waiting for a connecting client..."
isConnected = False
while True:
    debug("Calling blocking accept()...")
    conn, addr = serverSocket.accept()
    print "Connected with client at " + addr[0]
    isConnected = True
    socketHandler = SocketHandler(conn)
    # necessary to terminate it at program termination:
    socketHandler.setDaemon(True)  
    socketHandler.start()
    t = 0
    while isConnected:
        print "Server connected at", t, "s"
        time.sleep(10)
        t += 10