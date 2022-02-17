import socket


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # In case connection drop, retrieve it
listener.bind(("192.168.190.140", 4444))
listener.listen(0)  # the number of connection that can be queued
listener.accept()
