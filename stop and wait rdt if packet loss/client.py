import socket
import time

# Define server address and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set timeout value for socket
sock.settimeout(1)

# Define packet format
packet_fmt = "{} {}"

# Define sequence number
seq_num = 0

# Define data to be sent
data = ["Hello", "World", "Stop", "and", "Wait", "RDT", "Done"]

# Send SYN flag to server
sock.sendto(b"SYN", (UDP_IP, UDP_PORT))

# Wait for SYNACK flag from server
while True:
    try:
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "SYNACK":
            print("Received SYNACK flag from server")
            break
    except socket.timeout:
        print("Timeout waiting for SYNACK, retrying...")
        sock.sendto(b"SYN", (UDP_IP, UDP_PORT))

# Send ACK flag to server to start communication
sock.sendto(b"ACK", (UDP_IP, UDP_PORT))
print("Sent ACK flag to server, starting communication")

# Send data to server using Stop-and-wait RDT
for msg in data:
    # Construct packet with sequence number
    packet = packet_fmt.format(seq_num, msg).encode()
    
    # Send packet to server
    while True:
        sock.sendto(packet, (UDP_IP, UDP_PORT))
        print(f"Sent message {seq_num} to server")
        
        # Wait for ACK flag from server
        try:
            data, server_addr = sock.recvfrom(1024)
            if data.decode() == "ACK":
                print(f"Received ACK flag from server for message {seq_num}")
                break
        except socket.timeout:
            print(f"Timeout waiting for ACK flag for message {seq_num}, resending...")
            
    # Increment sequence number
    seq_num += 1

# Send FIN flag to server
sock.sendto(b"FIN", (UDP_IP, UDP_PORT))
print("Sent FIN flag to server")

# Wait for FINACK flag from server
while True:
    try:
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "FINACK":
            print("Received FINACK flag from server")
            break
    except socket.timeout:
        print("Timeout waiting for FINACK, retrying...")

# Close the socket
sock.close()
print("Socket closed")
