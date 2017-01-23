#!/usr/bin/env python2.7
'''
The Chat Client
'''
import select
import socket
import sys
from persist import connection


def get_user(username):
    uname = None
    try:
        cur = connection.cursor()
        # look for username
        sql = "SELECT * FROM users WHERE username = %(user)s"
        cur.execute(sql, {'user': username})
        result = cur.fetchone()
        if result:
            uname = result[1]
        else:
            raise
    except:
        # create a new user if user not found
        cur = connection.cursor()
        sql = "INSERT INTO users (username) VALUES (%(user)s)"
        cur.execute(sql, {'user': username})
        connection.commit()
        uname = username
    finally:
        connection.close()
    return uname


def all_users():
    '''
    Return all users
    '''
    try:
        cur = connection.cursor()
        sql = "SELECT username FROM users"
        cur.execute(sql)
        result = cur.fetchall()
        print result
        if len(result) > 0:
            for res in result:
                print(res[0])
    except:
        print('Haaaaaaaaaaaaa. You aint smarter')


def get_user_messages(user, num):
    try:
        cur = connection.cursor()
        sql = "SELECT message, sender FROM messages WHERE username = %s LIMIT %s"
        cur.execute(sql, (user, num))
        result = cur.fetchall()
        if len(result) > 0:
            for i, res in enumerate(result):
                i += 1
                print('{}: {} said {}'.format(
                    i, res['sender'], res['message']))
        else:
            print('Empty results')
    except:
        print('User not found. Try again')


def prompt():
    sys.stdout.write('You : ')
    sys.stdout.flush()


class ChatClient:

    def __init__(self, host, port, username):
        self.username = get_user(username)
        print username
        self.host = host
        self.port = port
        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to remote host
        try:
            self.csocket.connect((self.host, self.port))
        except:
            print('Unable to connect')

            sys.exit()

        print('You are Connected. username: message \n Please press C^out to quit')
        self.csocket.send(username.encode('utf-8'))
        prompt()

    def run(self):
        while True:
            socket_list = [sys.stdin, self.csocket]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(
                socket_list, [], [])

            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.csocket:
                    data = sock.recv(1024)
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        # print("\r", data.decode('utf-8'), end="")
                        prompt()

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    if msg.find(':') != -1:
                        self.csocket.send(msg.encode('utf-8'))
                    else:
                        print('The Format must be username: message ')
                    prompt()


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        if sys.argv[1] == 'users':
            all_users()
        else:
            print('Usage : python client.py users')
            sys.exit()

    elif(len(sys.argv) == 3):
        user = sys.argv[1]
        num = int(sys.argv[2])

        if num < 0:
            print('Number of messages show be a positive integer')
            print('Usage : python client.py username 10')
            sys.exit()
        get_user_messages(user, num)

    else:
        name = raw_input("Welcome! Enter your username : ")
        client_chat = ChatClient('127.0.0.1', 7000, name)
        client_chat.run()
