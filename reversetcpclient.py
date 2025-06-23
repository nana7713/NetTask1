from socket import *
import random
import os
import struct
def send_packet(sock, packet_type, data):
    # 构造头部：2字节类型 + 4字节长度
    header = struct.pack('>HI', packet_type, len(data))
    # 发送头部和数据
    sock.sendall(header + data)
serverName=input('please input server IP:')
serverPort=input('Please input server port:')
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,int(serverPort)))
file=open('source.txt',mode='r')
size=os.stat('source.txt').st_size
N=0
if size==0:
    print("文件不能为空！")
    exit()
       
print("文件大小为{}byte".format(size))
Lmin=int(input("请输入报文块的最小长度:"))
Lmax=int(input("请输入报文块的最大长度:"))
lens=[]

while True:
    if sum(lens)>=size:
        lens[-1]-=sum(lens)-size
        break
    l=random.randint(Lmin,Lmax)
    lens.append(l)
    N+=1
header=struct.pack('>HI',1,N)
clientSocket.sendall(header)
response=clientSocket.recv(2)
tempt=[]
ptype= struct.unpack('>H', response)[0]
if(ptype==2):
    reversedFile=open('reversedFile.txt',mode='w')
    for i in range(N):
        message=file.read(lens[i])
        send_packet(clientSocket,3,message.encode())
        answer_header = clientSocket.recv(6)  
        if len(answer_header) < 6:
             break
        ptype, length = struct.unpack('>HI', answer_header)
        reverseMessage=clientSocket.recv(length).decode()
        tempt.append(reverseMessage)
        print('{}:'.format(i+1),reverseMessage)
    for i in tempt[::-1]:
        reversedFile.write(i)
clientSocket.close()