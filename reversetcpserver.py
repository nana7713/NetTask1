from socket import *
import threading
import struct
def send_packet(sock, packet_type, data):
    # 构造头部：2字节类型 + 4字节长度
    header = struct.pack('>HI', packet_type, len(data))
    # 发送头部和数据
    sock.sendall(header + data)

def handle_client(connectionSocket):
    try:
        answer_header = connectionSocket.recv(6)
        ptype, N = struct.unpack('>HI', answer_header)
        header=struct.pack('>H',2)
        connectionSocket.sendall(header)
        for _ in range(N):
            request_header = connectionSocket.recv(6)
            if len(request_header) < 6:
                break
            ptype, length = struct.unpack('>HI', request_header)
            message = connectionSocket.recv(length).decode()
            reverseMessage = message[::-1]
            send_packet(connectionSocket,4,reverseMessage.encode())
    finally:
        connectionSocket.close()

serverPort = 8977
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)  
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"New connection from {addr}")
    threading.Thread(target=handle_client, args=(connectionSocket,)).start()