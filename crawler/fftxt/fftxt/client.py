#-*-coding:utf-8

import socket
s = ''


def socket_send(content):
    global s
    if not s:
        s = socket.socket()
        s.connect(('yiwanshu.com', 9000))
    s.sendall(content)
