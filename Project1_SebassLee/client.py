import socket
import threading
import time
from datetime import datetime


# enter nickname
def nameEnter():
    global nickname 
    nickname = input("Please enter a username: ")
    global client 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 18000))
    client.send(nickname.encode())
    while True:
        message = client.recv(1024).decode('ascii') # recieve reject or connect 
        if(message == 'reject' or message == 'nicknameError'):
            print("Chatroom is already full or Select different nickname.")
            client.close()
            return False #CONNECTION SUCESS BUT THERE ARE NO MORE SEATS
        else:
            return True #CONNECTION SUCESS AND SEATS ARE AVAILAVLE

# show the users and their information in chatroom
def showUserList():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 18000))
    client.send("LIST".encode())
    time.sleep(0.8)
    userList = client.recv(1024).decode('ascii')
    print(userList)
    client.close()

# read the user input file 
def readFile():
    print("Enter to read file.")
    file_name = input("Please enter the file path and name: ")
    with open(file_name) as f:
        lines = f.readlines()
        chatWrite(lines)
    f.close()
    print(lines)
    return lines

# includes message datetime and name
def chatWrite(message):
    new_message = f'{nickname}: {message}'
    date_now = datetime.now().strftime("[%H:%M] ")
    new_message = date_now + new_message
    client.send(new_message.encode('ascii'))

# get message from server
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if(chat_finished):
                break
            elif message == 'file':
                readFile()
                chatWrite(readFile())
            else:
                print(message)
        except:
            client.close()
            break

# write function to send message to chatroom
def write():
    global chat_finished 
    chat_finished = False
    recieve_thread = threading.Thread(target=recieve)
    recieve_thread.start()
    while True: # same as wrtie()
        message = input()
        if message.lower() == 'q':
            client.send(message.encode())
            chat_finished = True
            break 
        else:
            if message.lower() == 'a':
                client.send(message.encode())
            else: 
                chatWrite(message)

# give options to user
def giveOption():    
    while True:
        print("Please select one of the following options:\n    1.Get a report of the chatroom from the server.\n    2.Request to join the chatroom.\n    3.Quit the program")
        user_Option = input("Your choice: ")
        try:
            # if message is not empty, send it to server
            if not user_Option.isspace():
            # Option 1: get the list of clients in the server
                if user_Option == "1":
                    showUserList()
            
                # Option 2: join the chatroom
                elif user_Option == "2":
                    if(nameEnter()):
                        write()

                # Option 3: quit the chatroom 
                elif user_Option == "3":
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    return
                # wrong option case
                else:
                    print("Wrong option, choose again.")
                    #client_menu()
        except:
            print("System Error.")
            client.shutdown(socket.SHUT_RDWR)
            client.close()      
            return

def main_function():
    giveOption()         
# start client program
main_function()

    
