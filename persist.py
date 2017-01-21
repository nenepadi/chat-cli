#!/usr/bin/env python2.7

import mysql.connector as cnx

config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'chatcli',
    'user': 'root',
    'password': 'wfBAT@gh',
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}

connection = cnx.connect(**config)
