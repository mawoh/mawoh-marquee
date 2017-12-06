#!/usr/bin/env python3

"""
Wir bauen einen kleinen TCP Server und Client

TODO:

- [ ] TCP Server
- [ ] TCP Client
- [ ] Kommandozeile





"""

import os
import logging
import socket
import select
import argparse

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('tcp-demo')

class TcpServer(object):

    """
    simple echo server
    """

    def __init__(self, address, port):
        """
        constructor
        """
        self.address = address
        self.port = port
        self.buffersize = 1024
        self.maxconnections = 1

    def run(self):
        """
        - open socket
        - read from socket
        - write answer
        """

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.address,self.port))
        server.listen(self.maxconnections)
        log.info('listening on {}:{}'.format(self.address, self.port))

        read_list = [server]

        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is server:
                    conn, addr = s.accept()
                    log.info('new connection from: {}'.format(addr))
                    read_list.append(conn)
                else:
                    data = s.recv(self.buffersize)
                    if data:
                        log.info('received data: {}'.format(data))
                        s.send(data)
                    else:
                        s.close()
                        read_list.remove(s)

if __name__ == "__main__":
    server = TcpServer('127.0.0.1', 4567)
    server.run()
