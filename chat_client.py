#!/usr/bin/env python2.7


import sys
import socket
import select
from persist import get_or_create_user, get_user_messages, get_all_users


class Client:
    def __init__(self, host, port, user):
        self.user = get_or_create_user(user)
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

        try:
            self.client_socket.connect((self.host, self.port))
        except:
            print "Unable to connect on {}:{}".format(self.host, self.port)
            sys.exit()

        self.client_socket.send(user);
        sys.stdout.write('<=[You] '); sys.stdout.flush()


    def run(self):
        while True:
            socket_list = [sys.stdin, self.client_socket]

            # get all sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                if sock == self.client_socket:
                    # incoming message ...
                    data = sock.recv(1024)
                    if not data:
                        print "\nDisconnected from chat server"
                        sys.exit()
                    else:
                        # print data
                        sys.stdout.write(data)
                        sys.stdout.write("<=[You] "); sys.stdout.flush()
                else:
                    message = sys.stdin.readline()
                    self.client_socket.send(message)
                    sys.stdout.write("<=[You] "); sys.stdout.flush()


if __name__ == "__main__":
    # Run this way till you get chat based commands working
    if(len(sys.argv) == 2):
        if sys.argv[1] == 'users':
            get_all_users()
        else:
            print('Usage: python client.py users')
            sys.exit()

    elif(len(sys.argv) == 4):
        user = sys.argv[1]
        sender = sys.argv[2]
        num = int(sys.argv[3])

        if num < 0:
            print('Number of messages show be a positive integer')
            print('Usage : python client.py username sender 10')
            sys.exit()
        get_user_messages(user, sender, num)
    else:
        print "************************"
        print "COMMAND LINE CHAT CLIENT"
        print "************************\n"
        print "Menu:"
        print "-----"
        print "@server users => List all users"
        print "@server messages <user> <N> => List last N messages from user"
        print "@server quit => Disconnect your client connection\n"

        name = raw_input("Welcome, please tell us your name => ")
        c = Client("127.0.0.1", 9000, name)
        sys.exit(c.run())
