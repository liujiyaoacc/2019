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
ep=epoll()
ep.register(sockfd,EPOLLIN)
fdmap={sockfd.fileno():sockfd}
while True:
    print('等待就绪')
    events=ep.poll()
    print('你有新的IO需要处理哦',events)
    for fd,event in events:
        if fd==sockfd.fileno():
            connfd,addr=fdmap[fd].accept()
            print('connect from',addr)
            connfd.setblocking(False)
            ep.register(connfd, EPOLLIN)
            fdmap[connfd.fileno()]=connfd
        else:
            data=fdmap[fd].recv(1024).decode()
            if not data:
                ep.unregister(fd)
                fdmap[fd].close()
                del fdmap[fd]
                continue
            print(data)
            fdmap[fd].send(b'ok')

