import socket
import time

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

# Receive data from the client using Stop-and-wait RDT
packet_fmt = "{} {}"
expected_seq_num = 0

while True:
    # Receive packet from client
    data, client_addr = sock.recvfrom(1024)
    packet = data.decode()
    seq_num, msg = packet_fmt.format(packet[0], packet[2:]).split()

    # Check if packet has correct sequence number
    if int(seq_num) == expected_seq_num:
        print(f"Received message {seq_num} from client: {msg}")
        expected_seq_num += 1
        
        # Send ACK flag to client
        while True:
            sock.sendto(b"ACK", client_addr)
            print(f"Sent ACK flag for message {seq_num} to client")
            break
    else:
        print(f"Received duplicate message {seq_num} from client, resending ACK...")
        sock.sendto(b"ACK", client_addr)
        
    # Check if all messages have been received
    if expected_seq_num == len(packet_fmt.split()):
        break

# Wait for FIN flag from client
while True:
    data, client_addr = sock.recvfrom(1024)
    if data.decode() == "FIN":
        print("Received FIN flag from client")
        break

# Send FINACK flag to client
sock.sendto(b"FINACK", client_addr)
print("Sent FINACK flag to client")

# Close the socket
sock.close()
print("Socket closed")
