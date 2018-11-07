COMMAND LINE CHAT
==================

A commandline Chat Application

Installation
------------

```bash

    $ vagrant up
    $ vagrant ssh
```

Usage
-----

```bash
    # Show client's messages - ./client.py username sender no. of msgs
    $ python chat_client.py obed pius 10

    # Show all clients
    $ python chat_client.py users

    # Chat with user
    $ python chat_client.py

    # Enter username to register or login
    $ Welcome! Enter your username => obed

    # Send mention directly to another user
    <=[You] How are you? @ pius

    # Broadcast message
    <=[You] Hello, world!!!
```

N.B: The trials folder also has some awesome examples. Worked though but didnt meet requirements. A work in progress though.

ToDo List:
==========
* Implement server based commands. Instead of calling file with arguments, do it within the chat stream.

