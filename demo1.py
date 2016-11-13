# -*- coding=utf-8 -*-
import socket
import time

tic = lambda x: '\nat %1.1f second' % (time.time()-x)


def get_request(path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    sock.send('GET {} HTTP/1.0\r\n\r\n'.format(path).encode('utf-8'))
    buffer = []
    while True:
        chunk = sock.recv(10)
        if chunk:
            buffer.append(chunk)
        else:
            break

    sock.close()
    print(b''.join(buffer).decode('utf-8'))

s = time.time()
get_request('/index')
get_request('/index')
print(tic(s))
