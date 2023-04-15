import socket
import threading
import time
import pickle
from datetime import datetime

nickname = input("Please enter a username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 18000))

# get message from server
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

# write function to send message to chatroom
def write():
    while True:
        message = f'{nickname}: {input("")}'
        date_now = datetime.now().strftime("[%H:%M] ")
        message = date_now + message
        client.send(message.encode('ascii'))
           


# give options to user
def giveOption():
    try:
        print("Please select one of the following options:\n    1.Get a report of the chatroom from the server.\n    2.Request to join the chatroom.\n    3.Quit the program")
        user_Option = input("Your choice: ")
        
        # if message is not empty, send it to server
        if not user_Option.isspace():
        # Option 1: get the list of clients in the server
            if user_Option == "1":
                print("Here is the list: ")
                time.sleep(0.8)
                serverSend = client.recv(1024)
                serverList = pickle.loads(serverSend)
        
            # Option 2: join the chatroom
            elif user_Option == "2":
                recieve_thread = threading.Thread(target=recieve)
                recieve_thread.start()
                write_thread = threading.Thread(target=write)
                write_thread.start()

            # Option 3: quit the chatroom
            elif user_Option == "3":
                print("Leave the chatroom")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            # wrong option case
            else:
                print("Wrong option, choose again.")
                giveOption()   
    except:
        print("System Error.")
        client.shutdown(socket.SHUT_RDWR)
        client.close()      

# start client program
giveOption()


# recieve_thread = threading.Thread(target=recieve)
# recieve_thread.start()
# write_thread = threading.Thread(target=write)
# write_thread.start()

    
