"""
http 示例代码
"""
from socket import *

# tcp套接字
sockfd = socket()
sockfd.bind(('0.0.0.0',8000))
sockfd.listen(5)

connfd,addr = sockfd.accept()
print("Connect from",addr)

# 接收到来自浏览器的http请求
data = connfd.recv(4096)
print(data.decode())

with open("static/index.html",'r') as f:
    data = f.read()

response = "HTTP/1.1 200 OK\r\n" # http协议规定换行是\r\n
response += "Content-Type:text/html\r\n" # 响应头
response += "\r\n"  # 空行
# response += "Hello world!"
response += data

# 发送响应
connfd.send(response.encode())

connfd.close()
sockfd.close()