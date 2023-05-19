import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.bind((UDP_IP, UDP_PORT))  # bind socket to IP and port

while True:
    data, addr = sock.recvfrom(1024)  # receive data from client
    message = data.decode()
    print("received message:", message)

    # parse message to get method, path, and body
    method, path, body = "", "", ""
    if message:
        lines = message.split("\r\n")
        method, path, *_ = lines[0].split()
        body = lines[-1]
    
    # create response message
    if method == "GET" and path == "/":
        response_body = "<h1>Hello, World!</h1>"
        response_body = "<h1>Received GET request" + body + "</h1>\r\n\r\n"
        response_header = "HTTP/1.0 200 OK/Hello GET\r\nContent-Type: text/html\r\n\r\n"
    elif method == "POST" and path == "/":
        response_body = "<h1>Received POST request" + body + "</h1>\n"
        response_header = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
    else:
        response_body = "\n<h1>Not Found</h1>\n"
        response_header = "HTTP/1.0 404 NOT FOUND\r\nContent-Type: text/html\n"
    
    response_message = response_header.encode() + response_body.encode()
    sock.sendto(response_message, addr)  # send response back to client
