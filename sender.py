import hashlib
from math import floor
import os
import socket
import time
import flet
from flet import IconButton, Page, Row, TextField, icons
ip = ""
port = ""
file_path = ""
alertFunc = None
pluh = None
updateProgBar = None
def main(page: Page):
    global updateProgBar
    global file_path
    global ip
    global port
    global alertFunc
    global pluh
    newdlg = None
    ohioRizz = flet.Text("Waiting to transfer a file...", style="headlineSmall")
    progBarForNoReason = flet.ProgressBar(width=750)
    def updateProgBarFunny(percentlessthanone, x, y, speed):
        if x == -1:
            progBarForNoReason.value = None
            ohioRizz.value = "Waiting for the recipient to accept the transfer. Make sure the sender has the same code as you! Code: " + y
            page.update()
            return
        progBarForNoReason.value = percentlessthanone
        ohioRizz.value = "Transferring " + str(floor(x)) + " MB / " + str(floor(y)) + " MB at " + str(round(speed, 2)) + " Mbps..."
        if x == 0:
            progBarForNoReason.value = None
            ohioRizz.value = "Feel free to transfer another file! The last transfer went at a speed of " + str(round(speed, 2)) + " Mbps."
        page.update()
        return
    updateProgBar = updateProgBarFunny
    def pick_files_result(e: flet.FilePickerResultEvent):
        global file_path
        file_path = e.files[0].path
        print(file_path)
        send_file(file_path, ip, port)

    def gone():
        return
    pluh = gone
    def updateSettings(e):
        global file_path
        global ip
        global port
        ip = rizz.value
        port = int(fanum.value)
    page.horizontal_alignment = "center"
    page.title = "Dataline"
    page.vertical_alignment = "center"
    page.add(flet.Image("logo.png"))
    page.add(flet.Text("Dataline File Sender", size=50))
    page.add(flet.Text("Welcome! Set the IP and Port, and then click send and pick a file."))
    rizz = flet.TextField("", helper_text="IP Address", on_blur=updateSettings)
    fanum = flet.TextField("", helper_text="Port", on_blur=updateSettings)
    page.add(rizz)
    page.add(fanum)
    filePicker = flet.FilePicker(on_result=pick_files_result)
    page.overlay.append(filePicker)
    gyatt = flet.Text("File Name:")
    page.add(flet.TextButton("Send", scale=1.9, on_click=filePicker.pick_files))
    page.add(
        ohioRizz,
        progBarForNoReason,
    )
def send_file(file_path, server_ip, server_port):
    # Create a TCP socket
    global alertFunc
    global updateProgBar
    fanumTax = os.path.getsize(file_path) / (1024 * 1024)

    def hash_and_keep_numbers(input_string):
        # Hash the input string using SHA-256
        hashed = hashlib.sha256(input_string.encode()).hexdigest()

        # Extract only the numerical characters
        numbers = ''.join(filter(str.isdigit, hashed))

        return numbers[:6]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        client_socket.sendall(os.path.basename(file_path).encode("utf-8"))
        updateProgBar(0, -1, hash_and_keep_numbers(client_socket.getsockname()[0]), 0)
        # Open the file in binary mode
        i = 0
        with open(file_path, 'rb') as file:
            file_size = 0
            start_time = time.time()
            # Read the file data in chunks
            chunk = file.read(51200)
            client_socket.send(chunk)
            while chunk:
                i = i + 1
                # Send the chunk to the server
                chunk = file.read(51200)
                client_socket.send(chunk)
                file_size += len(chunk)
                if i % 200 == 0:
                    ohio = (file_size/1048576)/fanumTax
                    end_time = time.time()
                    time_taken = end_time - start_time  # in seconds
                    file_size_mb = file_size / (1024 * 1024)  # convert bytes to megabytes
                    transfer_speed_mbps = file_size_mb / time_taken
                    updateProgBar(ohio, file_size/1048576, fanumTax, transfer_speed_mbps*8)
            end_time = time.time()

            time_taken = end_time - start_time  # in seconds
            file_size_mb = file_size / (1024 * 1024)  # convert bytes to megabytes
            transfer_speed_mbps = file_size_mb / time_taken
            pluh()
            print(f"File sent successfully!")
            print(f"Transfer Speed: {transfer_speed_mbps:.2f} Mbps")
            updateProgBar(0, 0, fanumTax, transfer_speed_mbps*8)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the socket
        client_socket.close()

# Usage example
flet.app(target=main)