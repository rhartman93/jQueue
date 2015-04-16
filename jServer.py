import sys, socket, os, myQueue, threading, datetime
import OrderedSet as oSet

users = {}

    

jQueue = myQueue.myQueue()


startTime = datetime.datetime.now()
logName = "%d_%d_%d_%d_%d_log.txt" % (startTime.month, startTime.day, startTime.year, startTime.hour, startTime.minute)

logList = []


try:
    logFile = open(logName,"w") 
except:
    print "ERR: Failed to create log"

def menuPrint(other):
    #Used for status messages
    #Overwrites the existing line (Enter a Command), prints the message,
    #then reprints the prompt on the next line

    sys.stdout.write('\r' + other + "\nEnter a Command: ")
    sys.stdout.flush()
    #Using sys.stdout to avoid trailing newline. Flushing to ensure it all gets out

def checkUsers(uName, conn):
    #print "Checking Queue"
    resultMessage = "check\n"
    resultMessage += uName + "\n"
    if(uName in users.keys()):
        resultMessage += "exists"
        #print "exists"
    else:
        resultMessage += "new"
        #print "new"
    conn.sendall(resultMessage)

def addToQueue(connection, uName, uPass):
    #print "Am I even in here?"
    if uName in users and users[uName] == uPass:
        message = "queueAdd\n"
        succeed = jQueue.push(uName)
        #print str(succeed)
        if(succeed):
            #print "I guess it worked?"
            message += "success\n"
            connection.sendall(message)
        else:
            #print "Somehow the add still failed"
            message += "failed\n"
            connection.sendall(message)

def sendQueue(connection):
    qMessage = "queueShow\n"
    qMessage += jQueue.stringify()
    connection.sendall(qMessage)

def serveQueue():
    servedTime = datetime.datetime.now() #Might Add Time
    served = jQueue.serve()
    if served not in logList:
        logList.append(served)

def writeLog():
    global logFile
    for user in logList:
        logFile.write(user + "\n\n") 

def handleConnections(mySock):
    while 1:
        theirSock, address = mySock.accept()
        userThread = t = threading.Thread(target = createClientThread, args = (theirSock, address))
        t.daemon = True
        t.start()
        



def loadUserList():
    try:
        f = open("users.txt", "r")
        for line in f:
            if len(line) > 1:
                segment = line.split(" ")
                users[segment[0]] = segment[1].rstrip()
                #print users
        f.close()
    except:
        f = open("users.txt", "w")
        f.close()
        

def tryLogin(uName, uPass, uConnect):
    #print "User: " + uName + "\nPassword(Hashed): ", uPass
    message = "login\n"
    if uName in users and users[uName] == uPass:
        #print "Login Successful"
        message += "success\n"
        message += uName + "\n"
        message += uPass + "\n"
        uConnect.sendall(message)
    else:
        message += "failed"
        message += uName + "\n"
        message += uPass + "\n"
        uConnect.sendall(message)
        #print "Invalid Username or Password"

def addNewUser(uName, uPass):
    if uName not in users:
        f = open("users.txt", "w")
        for curUser in users.keys():
            f.write(curUser)
            f.write(" ")
            f.write(users[curUser])
            f.write("\n")
        f.write(uName)
        f.write(" ")
        f.write(uPass)
        f.write("\n")
        f.close()
        users[uName] = uPass
    #else:
        #print "User Already Exists"

def createClientThread(connection, theirAddr):
    menuPrint("Connection Established")
    stuff = connection.recv(1024)
    #print stuff
    lines = stuff.split("\n")
    while 1:
        lines = stuff.split("\n")
        #print "Lines: " + lines[0]
        if stuff == "":
            menuPrint("Connection Terminated by Client")
            #sys.exit()
            break
        if lines[0] == "check":
            checkUsers(lines[1], connection)
        if lines[0] == "register":
            addNewUser(lines[1], lines[2])
        if lines[0] == "login":
            tryLogin(lines[1], lines[2], connection)
        if lines[0] == "queueAdd":
            #print "trying to add " + lines[1] + " to queue\n"
            addToQueue(connection, lines[1], lines[2])
        if lines[0] == "queueShow":
            sendQueue(connection)
        stuff = connection.recv(1024)
        #print stuff

if len(sys.argv) <> 2:
    print "Invalid Number of Arguments"
    sys.exit()

loadUserList()


mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mySock.bind((socket.gethostname(), int(sys.argv[1])))
print "Hostname: " + socket.gethostname()
mySock.listen(5)

#if jQueue.isEmpty():
#    print "Queue Empty"
t = threading.Thread(target = handleConnections, args = (mySock,))
t.daemon = True
t.start()

whatDo = raw_input("Enter Command: ")
while 1:
    if whatDo.lower() == "p":
        print "Printing Queue..."
        print jQueue.print_()
        if jQueue.isEmpty():
            print "Queue Empty"
    elif whatDo.lower() == "r":
        jQueue.remove(0)
        #Using remove so they won't be written to attendance file
    elif whatDo.lower() == "s":
        serveQueue()
    elif whatDo.lower() == "q":
        print "Terminating Server"
        logFile.close()
        break
    whatDo = raw_input("Enter Command: ")
mySock.close()
