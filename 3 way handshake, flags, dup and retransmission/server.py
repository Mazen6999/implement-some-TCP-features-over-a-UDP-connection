import socket

# Define server address and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
sock.bind((UDP_IP, UDP_PORT))

# Wait for SYN flag from client and send SYNACK flag
while True:
    data, client_addr = sock.recvfrom(1024)
    if data.decode() == "SYN":
        print("Received SYN flag from client")
        sock.sendto(b"SYNACK", client_addr)
        print("Sending SYNACK flag to client")
        break

# Wait for ACK flag from client and start communication
data, client_addr = sock.recvfrom(1024)
if data.decode() == "ACK":
    print("Received ACK flag from client, starting communication")

# Receive data from the client and send ACK flag
expected_seq_num = 0
while True:
    data, client_addr = sock.recvfrom(1024)
    seq_num = int(data.decode().split()[1])
    if seq_num == expected_seq_num:
        print(f"Received message {seq_num} from client")
        sock.sendto(b"ACK", client_addr)
        expected_seq_num += 1
    else:
        print(f"Received duplicate message {seq_num} from client, discarding")
    if seq_num == 9:
        break

# Wait for FIN flag from client and send FINACK flag
while True:
    data, client_addr = sock.recvfrom(1024)
    if data.decode() == "FIN":
        print("Received FIN flag from client")
        sock.sendto(b"FINACK", client_addr)
        print("Sending FINACK flag to client")
        break

# Close the socket
sock.close()
print("Socket closed")
