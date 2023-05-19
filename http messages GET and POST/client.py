import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# send GET request
print("Send GET")
GET_request = "GET / HTTP/1.0\r\nHost: " + UDP_IP + ":" + str(UDP_PORT) + "\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello GET" + "\r\n\r\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.sendto(GET_request.encode(), (UDP_IP, UDP_PORT))  # send message to server
data, addr = sock.recvfrom(1024)  # receive response from server
print("received message:", data.decode())  # print received message
sock.close()  # close socket

# send POST request
print("Send POST")
POST_request = "POST / HTTP/1.0\r\nHost: " + UDP_IP + ":" + str(UDP_PORT) + "\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello POST" + "\r\n\r\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.sendto(POST_request.encode(), (UDP_IP, UDP_PORT))  # send message to server
data, addr = sock.recvfrom(1024)  # receive response from server
print("received message:", data.decode())  # print received message
sock.close()  # close socket

# send request NOT FOUND
print("Send Error")
GET_request = "Error / HTTP/1.0\r\nHost: " + UDP_IP + ":" + str(UDP_PORT) + "\r\n\r\n"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.sendto(GET_request.encode(), (UDP_IP, UDP_PORT))  # send message to server
data, addr = sock.recvfrom(1024)  # receive response from server
print("received message:", data.decode())  # print received message
sock.close()  # close socket