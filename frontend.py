import backend
from tkinter import *
import backend
import threading

# start message receiving server
def start_server():
    backend.receive_msg()

# send message to user
def send_message(recipient, message):
    backend.send_msg(recipient, message)
    

currentUser = 'none'


# create window
window = Tk()
window.title("Chat App")
window.geometry("500x500")

# create labels
recipient_label = Label(window, text="Connect to user: ")
recipient_label.grid(row=0, column=0)

# create entry boxes
recipient_entry = Entry(window)
recipient_entry.grid(row=0, column=1)

def connect():
    global currentUser
    currentUser = recipient_entry.get()
    recipient_entry.delete(0, END)
    recipient_label.config(text="Connected to " + currentUser)

    # create message box
    message_box = Text(window, height=20, width=50)
    message_box.grid(row=1, column=0, columnspan=3)
    
    # populate message box
    try:
        message_box.insert(END, "Connected to " + currentUser + " @" + backend.get_user_ip(currentUser))
        message_box.config(state=DISABLED)
    except:
        message_box.insert(END, "Error: User '" + currentUser + "' not found.")
        message_box.config(state=DISABLED)
    for message in backend.get_msg(currentUser):
        message_box.config(state=NORMAL)
        message_box.insert(END, '\n' + message[0] + ": "+ message[1] + " @" + message[2])
        message_box.config(state=DISABLED)
    
    # create message entry box
    message_entry = Entry(window, width=50)
    message_entry.grid(row=2, column=0, columnspan=2)

    # create send button
    send_button = Button(window, text="Send", command=lambda: send_message(currentUser, message_entry.get()))
    send_button.grid(row=2, column=2)




# create connect button
connect_button = Button(window, text="Connect", command=lambda: connect())
connect_button.grid(row=0, column=2)

# start server
server_thread = threading.Thread(target=start_server)
server_thread.start()

# start window
window.mainloop()
