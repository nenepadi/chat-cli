#!/usr/bin/env python2.7


import sys
import socket
import select
from persist import save_message


HOST = ''
RECV_BUFFER = 1024
PORT = 9000


class Server:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, self.port))
        self.server_socket.listen(5)

        # add server socket object to the dictionary of readable connections
        self.socket_list = {}
        self.socket_list[self.server_socket] = 'server'

        print "Chat server started on port {}".format(self.port)


    def accept_new(self):
        new_socket, new_addr = self.server_socket.accept()
        user = new_socket.recv(RECV_BUFFER)
        self.socket_list[new_socket] = user
        print "Client ({}, {}) is online".format(new_addr, user)
        self.broadcast(new_socket, "\r=>[server] {} is online\n".format(user))


    def run(self):
        while True:
            ready_to_read, ready_to_write, in_error = select.select(self.socket_list.keys(), [], [], 0)
            for sock in ready_to_read:
                # a new connection request received
                if sock == self.server_socket:
                    self.accept_new()
                else:
                    try:
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            _user = self.socket_list[sock]

                            if data.find('@') != -1:
                                online = False
                                _to = data.split('@')[1].strip()
                                for k, v in self.socket_list.items():
                                    if v == data.split('@')[1].strip():
                                        _to = k
                                        online = True
                                        break
                                self.send_message(data.split('@')[0].strip(), _to, _user, online)
                            else:
                                self.broadcast(sock, "\r=>[{}] {}".format(str(sock.getpeername()), data))
                        else:
                            if sock in self.socket_list.keys():
                                del self.socket_list[sock]

                            self.broadcast(sock, "{} is offline\n".format(self.socket_list[sock]))
                    except:
                        self.broadcast(sock, "{} is offline\n".format(self.socket_list[sock]))
                        continue

        self.server_socket.close()


    def broadcast(self, omit_sock, message):
        for sock in list(self.socket_list):
            # send message only to peer
            if sock != self.server_socket and sock != omit_sock:
                try:
                    sock.send(message)
                except:
                    # a broken connection
                    sock.close()
                    del self.socket_list[sock]


    def send_message(self, message, reciever, sender, online):
        modified_message = "\r=>[{}] {}".format(sender, message.strip())

        if online:
            reciever.send(modified_message + "\n")
            reciever_name = self.socket_list[reciever]

        save_message(message.lstrip(), reciever_name, sender)


if __name__ == "__main__":
    s = Server(PORT)
    sys.exit(s.run())
