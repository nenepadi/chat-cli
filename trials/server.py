#!/usr/bin/env python2.7
'''
The Chat Server
'''
import select
import socket
from persist import connection


def save_message(message, user, sender):
    try:
        cur = connection.cursor()
        stmt_insert = "INSERT INTO messages (username, message, sender) VALUES (%s, %s, %s)"
        cur.execute(stmt_insert, (user, message, sender))
        connection.commit()
    except Exception as e:
        print(e)
        print('Didn\'t save. Try Again')


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('', self.port))
        self.sockserver.listen(5)

        self.connectors = {}
        self.connectors[self.sockserver] = 'server'
        print('Chatserver started on port {}'.format(self.port))

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.connectors.keys(), [], [])

            for sock in read_sockets:

                if sock == self.sockserver:
                    self.accept_new_connection()
                else:
                    # Data recieved from client, process it
                    try:
                        data = sock.recv(1024)
                        if data:
                            _user = self.connectors[sock]
                            msg = data.decode('utf-8')
                            if msg.find(':') != -1:
                                online = False
                                _to = msg.split(':')[0]
                                for k, v in self.connectors.items():
                                    if v == msg.split(':')[0]:
                                        _to = k
                                        online = True
                                        break
                                self.send_message(
                                    msg.split(':')[1], _to, _user, online)
                            else:
                                newstr = '{}'.format(data)
                                self.broadcast_string(newstr, sock)

                    except:
                        # _user = sock.getpeername()
                        # status = '{} left \r\n'.format(_user)
                        # self.broadcast_string(status, sock)
                        # sock.close()
                        # del self.connectors[sock]
                        continue

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.sockserver.accept()
        username = newsock.recv(1024).decode('utf-8')
        self.connectors[newsock] = username
        status = '{} is online \r\n'.format(username)
        self.broadcast_string(status, newsock)

    def broadcast_string(self, msg, omit_sock):
        for sock in list(self.connectors):
            if sock != self.sockserver and sock != omit_sock:
                try:
                    sock.send(msg.encode('utf-8'))
                except:
                    sock.close()
                    del self.connectors[sock]

    def send_message(self, msg, receiver, sender, online):
        modified_msg = '{} > {}'.format(sender, msg.lstrip())
        reciever_name = receiver
        if online:
            receiver.send(modified_msg.encode('utf-8'))
            reciever_name = self.connectors[receiver]
        save_message(msg.lstrip(), reciever_name, sender)


if __name__ == '__main__':
    serv_chat = ChatServer(7000)
    serv_chat.run()
