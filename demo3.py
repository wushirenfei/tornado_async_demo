# -*- coding=utf-8 -*-
import selectors
import socket
import time

tic = lambda x: '\nat %1.1f second' % (time.time()-x)
slct = selectors.DefaultSelector()
request_numb = 0


class Feature(object):

    def __init__(self):
        self.callbacks = []

    def resolve(self):
        for callback in self.callbacks:
            callback()


def coroutine(func):

    def wrapper(*args, **kwargs):
        def run(generator):
            try:
                feature = next(generator)
                feature.callbacks.append(lambda: run(generator))
            except StopIteration:
                pass
        generator = func(*args, **kwargs)
        run(generator)

    return wrapper


@coroutine
def get_request(path):
    global request_numb
    request_numb += 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)

    try:
        sock.connect(('localhost', 8080))
    except BlockingIOError:
        pass

    f = Feature()
    # callback = lambda: connected(sock, path)
    # f.callbacks.append(callback)
    slct.register(sock.fileno(), selectors.EVENT_WRITE, f)
    yield f

# def connected(sock, path):
    slct.unregister(sock.fileno())
    sock.send('GET {} HTTP/1.0\r\n\r\n'.format(path).encode('utf-8'))

    buffer = []
    f = Feature()
    # callback = lambda: readable(sock, buffer)
    # f.callbacks.append(callback)
    slct.register(sock.fileno(), selectors.EVENT_READ, f)
    yield f

# def readable(sock, buffer):
#     global request_numb
    while True:
        slct.unregister(sock.fileno())
        chunk = sock.recv(128)
        if chunk:
            buffer.append(chunk)
            f = Feature()
            # callback = lambda: readable(sock, buffer)
            # f.callbacks.append(callback)
            slct.register(sock.fileno(), selectors.EVENT_READ, f)
            yield f
        else:
            sock.close()
            request_numb -= 1
            print(b''.join(buffer).decode('utf-8').split()[0])
            break

s = time.time()
get_request('/index')
get_request('/index')

while request_numb:
    events = slct.select()
    for key, mask in events:
        f = key.data
        f.resolve()

print(tic(s))
