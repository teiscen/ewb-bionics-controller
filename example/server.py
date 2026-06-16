# test_server.py
import socket
import struct

# ----- THIS IS JUST SOMETHING REQUIRED FOR THE EXAMPLE

HOST = 'localhost'
PORT = 50007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f'Test server listening on {HOST}:{PORT}')

while True:
    data, addr = sock.recvfrom(1024)
    finger, curl = struct.unpack('Bh', data)
    print(f'Received from {addr}: finger={finger} curl={curl}')