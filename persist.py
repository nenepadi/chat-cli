#!/usr/bin/env python2.7

import mysql.connector as cnx
import sys


config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'chatcli',
    'user': 'root',
    'password': 'admin',
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}

connection = cnx.connect(**config)
cur = connection.cursor()


def save_message(msg, user_to, user_from):
    try:
        sql = "INSERT INTO messages (username, message, sender) VALUES(%(username)s, %(message)s, %(sender)s)"
        cur.execute(sql, {'username':user_to, 'message':msg, 'sender':user_from})
        connection.commit()
    except:
        print "Didn't save. Try again!!!\n"


def get_or_create_user(username):
    user = None
    try:
        # search user by name
        sql = "SELECT * FROM users WHERE username = %(username)s"
        cur.execute(sql, {'username':username})
        result = cur.fetchone()
        if result:
            user = result[1]
        else:
            raise
    except:
        # user not found? create user
        sql = "INSERT INTO users (username) VALUES (%(username)s)"
        cur.execute(sql, {'username': username})
        connection.commit()
        user = username
    finally:
        connection.close()

    return user


def get_all_users():
    try:
        sql = "SELECT username FROM users"
        cur.execute(sql)

        print "\nThe following are or have been in the chat room before:"
        for user in cur.fetchall():
            print user[0]
    except:
        print "There are no users at all"
    finally:
        connection.close()


def get_user_messages(user, user_from, number):
    try:
        sql = "SELECT message FROM messages WHERE username = %(username)s AND sender = %(sender)s LIMIT %(num)s"
        cur.execute(sql, {'username':user, 'sender':user_from, 'num':number})
        messages = cur.fetchall()

        print "\nThese are the last {} messages from {}".format(number, user_from)
        if len(messages) > 0:
            for message in messages:
                print "{} => {}".format(user_from, message[0])
        else:
            print "There are no messages from {}".format(user_from)
    except:
        print "User not found. Try again!!!"
    finally:
        connection.close()
