# -*- coding=utf-8 -*-
import selectors
import socket
import time

tic = lambda x: '\nat %1.1f second' % (time.time()-x)
slct = selectors.DefaultSelector()
request_numb = 0


def get_request(path):
    global request_numb
    request_numb += 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        sock.connect(('localhost', 8080))
    except BlockingIOError:
        pass

    callback = lambda: connected(sock, path)
    slct.register(sock.fileno(), selectors.EVENT_WRITE, callback)


def connected(sock, path):
    slct.unregister(sock.fileno())
    sock.send('GET {0} HTTP/1.0\r\n\r\n'.format(path).encode('utf-8'))
    buffer = []
    callback = lambda: readable(sock, buffer)
    slct.register(sock.fileno(), selectors.EVENT_READ, callback)


def readable(sock, buffer):
    global request_numb
    slct.unregister(sock.fileno())
    chunk = sock.recv(10)
    if chunk:
        buffer.append(chunk)
        callback = lambda: readable(sock, buffer)
        slct.register(sock.fileno(), selectors.EVENT_READ, callback)
    else:
        sock.close()
        print(b''.join(buffer).decode('utf-8'))
        request_numb -= 1

s = time.time()
get_request('/index')
get_request('/index')

while request_numb:
    events = slct.select()
    for key, mask in events:
        callback_fn = key.data
        callback_fn()

print(tic(s))
