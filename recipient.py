import socket
import threading
import flet
import flet as ft
import os
from flet import IconButton, Page, Row, TextField, icons
file_path = "Downloads"
link_func = None
acceptance = False
globalIndicator = None
trueAcceptance = False
import hashlib

def hash_and_keep_numbers(input_string):
    # Hash the input string using SHA-256
    hashed = hashlib.sha256(input_string.encode()).hexdigest()

    # Extract only the numerical characters
    numbers = ''.join(filter(str.isdigit, hashed))

    return numbers[:6]
def blud():
    def handle_client(client_socket, file_path):
        global globalIndicator
        with open(file_path, 'wb') as file:
            while True:
                file_data = client_socket.recv(51200)
                if not file_data:
                    break
                file.write(file_data)
        client_socket.close()
        globalIndicator("Waiting for a file transfer...", False)
    global link_func
    global file_path
    global trueAcceptance
    global acceptance
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and port
    host = '0.0.0.0'
    port = 12345

    
    # Bind the socket to the host and port
    try:
        server_socket.bind((host, port))
    except:
        server_socket.close()
        server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(1)

    print('Server is listening for incoming connections...')

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        recver = client_socket.recv(51200)
        filename = recver.decode("utf-8")
        globalIndicator("Waiting to start transferring "+filename+"...", False)
        print("Triggering request!")
        link_func(client_address[0])
        print(client_address[0])
        while True:
            if acceptance == True:
                break
        globalIndicator("Currently transferring "+filename+" to " + file_path, True)
        print('Connected to client:', client_address)
        # Specify the file path to save the received file
        # Create a new thread to handle the client
        if trueAcceptance == True:
            client_thread = threading.Thread(target=handle_client, args=(client_socket, os.path.join(file_path, filename)))
            client_thread.start()
        else:
            server_socket.close()
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.listen(7)
        acceptance = False
        trueAcceptance = False


def main(page: Page):
    global file_path
    global link_func
    global acceptance
    global trueAcceptance
    global globalIndicator
    rizzler = None
    fanumTaxersA = flet.Text("Waiting to transfer a file...", style="headlineSmall")
    progBarForNoReason = flet.ProgressBar(width=750,value=1)
    def accept(e):
        global rizzler
        global acceptance
        global trueAcceptance
        rizzler.open = False
        page.update()
        acceptance = True
        trueAcceptance = True
    def decline(e):
        global rizzler
        global acceptance
        global trueAcceptance
        rizzler.open = False
        page.update()
        acceptance = True
        trueAcceptance = False
    def hi(help):
        global rizzler
        print("Recieved")
        rizzler = ft.CupertinoAlertDialog(
            title=ft.Text("Accept Incoming Connection"),
            content=ft.Text("Would you like to accept an incoming file? To verify the identity of the sender, make sure the code matches. Code: "+hash_and_keep_numbers(help)),
            actions=[
                ft.CupertinoDialogAction(
                    "Accept",
                    is_destructive_action=True,
                    on_click=accept
                ),
                ft.CupertinoDialogAction(text="Decline", on_click=decline),
            ],
        )
        page.dialog = rizzler
        rizzler.open = True
        page.update()
    def updateModule(str, active):
        if active == True:
            fanumTaxersA.value = str
            progBarForNoReason.value = None
        if active == False:
            fanumTaxersA.value = str
            progBarForNoReason.value = 1
        page.update()
    globalIndicator = updateModule
    def gyattRizzLink(e):
        global file_path
        dir = ""
        file_path = dir
        print(file_path)
    link_func = hi
    page.horizontal_alignment = "center"
    page.title = "Dataline"
    page.vertical_alignment = "center"
    page.add(flet.Image("logo.png"))
    page.add(flet.Text("Dataline File Reciever", size=50))
    page.add(flet.Text("Select save location and keep this window open to recieve data!"))
    IPaddr = socket.gethostbyname(socket.gethostname())
    page.add(flet.Text("Your IP Address: "+IPaddr))
    page.add(flet.Text("Your Port: 12345"))
    page.add(fanumTaxersA)
    page.add(progBarForNoReason)

    blud()
flet.app(target=main)
