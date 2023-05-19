import socket

# Define server address and port
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the timeout for the socket to 10 seconds
sock.settimeout(10)

# Send SYN flag to server and wait for SYNACK flag
while True:
    sock.sendto(b"SYN", (UDP_IP, UDP_PORT))
    print("Sending SYN flag to server")
    try:
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "SYNACK":
            print("Received SYNACK flag from server")
            break
    except socket.timeout:
        print("Timed out waiting for SYNACK flag from server")
        continue

# Send ACK flag to server and start communication
sock.sendto(b"ACK", (UDP_IP, UDP_PORT))
print("Sending ACK flag to server and starting communication")

# Send data to the server and wait for ACK flag
seq_num = 0
while True:
    message = f"Message {seq_num}"
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Sending message {seq_num} to server")
    try:
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "ACK":
            print(f"Received ACK flag from server for message {seq_num}")
            seq_num += 1
        else:
            print(f"Received unknown flag {data.decode()} from server")
    except socket.timeout:
        print(f"Timed out waiting for ACK flag for message {seq_num}, retransmitting")
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        continue

    # Handle duplicate packet
    if seq_num > 0 and seq_num % 3 == 0:
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Resending message {seq_num} to server due to duplicate packet")

    # Handle end of communication
    if seq_num == 10:
        break

# Send FIN flag to server and wait for FINACK flag
sock.sendto(b"FIN", (UDP_IP, UDP_PORT))
print("Sending FIN flag to server")
while True:
    try:
        data, server_addr = sock.recvfrom(1024)
        if data.decode() == "FINACK":
            print("Received FINACK flag from server")
            break
    except socket.timeout:
        print("Timed out waiting for FINACK flag from server")
        continue

# Close the socket
sock.close()
print("Socket closed")
