# Ning Yi, CIS 345, TUTH 10:30, A8
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect the server, and change the button to disconnect
def connect_server():
    global IP, ScreenName, Background, connect_btn, ConnectBtn, message_frame, win,client_socket
    print(IP.get())
    if len(IP.get()) > 6 and ScreenName.get() is not None:
        ip = IP.get()
        ADDR = (ip, 49000)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
        try:
            client_socket.send(ScreenName.get().encode())
        except:
            client_socket.close()
            client_socket = None
        else:
            X = Thread(target=lambda: receive_func(), daemon=True)
            X.start()
            win.geometry('390x370')
            connect_btn['bg'] = 'Orange'
            ConnectBtn.set('Disconnect')
            connect_btn['command'] = disconnect
            message_frame.grid(row=3, column=0, columnspan=2, padx=10, sticky=NSEW)
            message_frame.pack_propagate(0)
    else:
        messagebox.showinfo('Error', 'Error, you must enter ')


# Disconnect the server, and change the button to connect
def disconnect():
    global IP, ScreenName, ConnectBtn, win, message_frame, client_socket,connect_btn
    try:
        client_socket.send('[Q]')
    except:
        pass
    finally:
        client_socket.close()
        client_socket = None
        connect_btn['bg'] = 'SystemButtonFace'
        ConnectBtn.set('Connect')
        connect_btn['command'] = connect_server
        message_frame.grid_forget()
        win.geometry('390x75')
        list_box.delete(0, END)


# Receive message from server
def receive_func():
    global ScreenName, client_socket
    while True:
        try:
            receive = client_socket.recv(1024)
        except OSError:
            receive = None
            break
        else:
            if receive is None:
                disconnect()
                break
        list_box.insert(END, receive.decode())


# send message to server
def send_func():
    global client_socket, message_entry, message
    data = message.get()
    if data == '[Q]':
        disconnect()
    try:
        client_socket.send(data.encode())
    except OSError:
        disconnect()
    message.set('')


# disconnect the client if the user close the window with out disconnect first
def window_closing():
    if client_socket is not None:
        disconnect()
    win.quit()


# only allowed key can be typed into IP entry
def key(event):
    global IP
    valid_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '\b', '']
    if event.char not in valid_keys:
        return 'break'


# when user click the message entry, empty the previous text
def empty(*args):
    message.set('')


win = Tk()
win.geometry('390x75')
win.title('CIS IM Client')

# IP entry and label layout
IP = StringVar()
ServerIP_label = Label(win, text='Server IP:', font=3)
ServerIP_label.grid(row=0, column=0)
ServerIP_entry = Entry(win, textvariable=IP, font=3, width=25)
ServerIP_entry.grid(row=0, column=1)
ServerIP_entry.bind("<Key>", key)

# Screen name entry and label layout
ScreenName = StringVar()
ScreenName_label = Label(win, text='Screen Name:', font=3)
ScreenName_label.grid(row=1, column=0)
ScreenName_entry = Entry(win, textvariable=ScreenName, font=3, width=25)
ScreenName_entry.grid(row=1, column=1)

# Connect button layout
ConnectBtn = StringVar()
ConnectBtn.set('Connect')
connect_btn = Button(win, textvariable=ConnectBtn, width=40, command=connect_server)
connect_btn.grid(row=2, columnspan=2, pady=1)

# message frame
message_frame = Frame(win, width=20,bg='sky blue', height=200, relief=SUNKEN)

# scrollbar and listbox layout
scrollbar = Scrollbar(message_frame)
list_box = Listbox(message_frame, width=25, height=10, yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)
scrollbar.grid(row=0, column=2,sticky=W,ipady=100,pady=5)
list_box.grid(row=0, column=0,columnspan=2,sticky=NSEW,ipadx=100,pady=5)

# message and send message button
message = StringVar()
message.set('Type your message here.')
message_entry = Entry(message_frame, textvariable=message)
message_entry.grid(row=1, column=0, sticky=NW,ipadx=95,ipady=4)
message_entry.bind('<Button-1>', empty)
send_btn = Button(message_frame, text='Send',command=send_func)
send_btn.grid(row=1,column=1,sticky=NW,columnspan=2,ipadx=10)


win.protocol("WM_DELETE_WINDOW", window_closing)
win.mainloop()
