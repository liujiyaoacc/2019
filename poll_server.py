"""
poll方法实现 tcp IO并发模型

建立字典用于通过文件描述符查找对象 fileno()

"""

from socket import *
from select import *

# 创建监听套接字，让客户端链接
sockfd = socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(3)

# IO多路复用通常配合非阻塞IO 防止网络延迟带来的长时间阻塞
sockfd.setblocking(False)

# 生成poll对象
p = poll()

# 设置关注的IO对象
p.register(sockfd,POLLIN)

# 建立 文件描述符 --》 IO对象的查找字典
# 要与关注的IO保持一直
fdmap = {sockfd.fileno():sockfd}

# 循环监控IO发生
while True:
    print("等待IO就绪。。。")
    events = p.poll() # 监控
    # 循环遍历，哪个IO就绪就处理哪个 events --> [(fd,event),..]
    for fd,event in events:
        # 监听套接字 接收客户端链接
        if fd == sockfd.fileno():
            connfd, addr = fdmap[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            # 增加关注的IO
            p.register(connfd,POLLIN)
            fdmap[connfd.fileno()] = connfd # 同时维护字典
        else:
            # 客户端链接套接字就绪
            data = fdmap[fd].recv(1024).decode()
            if not data:
                p.unregister(fd)  # 不在关注这个客户端
                fdmap[fd].close()
                del fdmap[fd] # 同时维护字典
                continue
            print(data)
            fdmap[fd].send(b'OK')

