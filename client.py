import sys, socket, os, hashlib, binascii

if len(sys.argv) <> 3:
    print "Invalid Number of Arguments"
    sys.exit()

hasher = hashlib.md5()
#Host and Port of server must be specified

serverAddr = (sys.argv[1], int(sys.argv[2]))
currentUser = () #Will fill with username and password. This will be used
                   #to validate that a queue request actually came from the
                   #person logged in


def requestQueue(server):
    message = "queueShow"
    server.sendall(message)
    daQueue = server.recv(10204)
    if daQueue.split("\n")[0] == "queueShow":
        return daQueue
    else:
        return "Garbage"
    

def sendToQueue(server):
    message = "queueAdd\n"
    message += currentUser[0] + "\n"
    message += currentUser[1] + "\n"
    #print message
    try:
        server.sendall(message)
    except:
        print "Err: SEND QueueAdd FAILED"

    response = server.recv(1024)
    #print response
    lines = response.split("\n")
    if lines[1] == "success":
        print "Successfully Added To Queue!"
    else:
        print "You're already in the queue, be patient!" #will have to update if more failure poitns occur
def CreateSession(server):
    stuff = server.recv(1024)
    #print stuff
    lines = stuff.split("\n")
    while stuff != "":
        if stuff == "":
            print "Lost connection to Server"
            break
        elif lines[0] == "login":
            if lines[1] == "success":
                print "Login Successful\n"
                global currentUser
                currentUser = (lines[2], lines[3])
                userInput = raw_input("(H)elp Me!\n(S)how Me The Queue\n(Q)uit")
                while 1:
                    if userInput.lower() == "h":
                        #print "Add to queue"
                        sendToQueue(server)
                    elif userInput.lower() == "s":
                        print requestQueue(server)
                    elif userInput.lower() == "q":
                        return
                    userInput = raw_input("(H)elp Me!\n(S)how Me The Queue\n(Q)uit")
            else:
                print "Invalid username or password"
                Password = raw_input("Enter password: ")
                #reHasher = None
                reHasher = hashlib.md5()
                reHasher.update(Password)
                Hashword = reHasher.hexdigest()
                logMessage = "login\n"
                logMessage += UserName + "\n"
                logMessage += Hashword
                server.sendall(logMessage)
                
        stuff = server.recv(1024)
        lines = stuff.split("\n")
        #print stuff


serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.connect(serverAddr)

#newUser = raw_input("Are you a new user?")

UserName = os.environ["USER"]

print "Welcome " + UserName

checkMessage = "check\n"
checkMessage += UserName
serverSock.sendall(checkMessage)

check = serverSock.recv(1024).split("\n")
if(check[1] == UserName):

    if check[2] == "new":
        print "Seems like this is your first time"
        newPassword = raw_input("Create a password (not your school password): ")
        hasher.update(newPassword)
        passHash = hasher.hexdigest()
        #print UserName + " : " + newPassword + " #", passHash
        newMessage = "register\n"
        newMessage += UserName + "\n"
        newMessage += passHash
        serverSock.sendall(newMessage)
    elif check[2] == "exists":
        Password = raw_input("Enter password: ")
        reHasher = hashlib.md5()
        reHasher.update(Password)
        Hashword = reHasher.hexdigest()
        logMessage = "login\n"
        logMessage += UserName + "\n"
        logMessage += Hashword
        #print logMessage
        serverSock.sendall(logMessage)
    CreateSession(serverSock)


    

print "Goodbye!"
serverSock.close()

