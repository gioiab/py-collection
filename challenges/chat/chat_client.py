"""
Created on 23/11/2015

@author: gioia

This script runs a simple ChatClient built with sockets.

The code is organized as follows:
- the ChatClient class defines the behaviour of the client;
- the main module function simply executes the server.

The programming language used is Python 2.7 and it is assumed you have it installed into your PC.
The operating system of reference is Linux. There are two basic ways to execute this script in Linux:
1 - launching it by the command shell through the python command;
2 - making it executable first and then launching it by the command shell.


Enjoy!
"""
import sys
import math
import struct
import socket
import select
import threading

_HOST = '127.0.0.1'  # defines the host as "localhost"
_PORT = 10000        # defines the port as "10000"

class ChatClient(threading.Thread):

    RECV_BUFFER = 4096  # defines the size (in bytes) of the receiving buffer
    RECV_MSG_LEN = 4  # defines the size (in bytes) of the placeholder contained at the beginning of the messages

    def __init__(self, host, port):
        """
        Initializes a new ChatClient
        :param host: the host on which the client connects
        :param port: the port on which the client connects
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.running = True
        self.client_socket = None

    def _connect(self):
        """
        Creates the client socket and connects it to the given host and port.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            print 'Unable to connect.'
            sys.exit()
        print 'Connected to remote host. Start sending messages.'

    def _prompt(self):
        """
        Simply writes the prompt.
        """
        sys.stdout.write('<You> ')
        sys.stdout.flush()

    def _send(self, msg):
        """
        Prefixes each message with a 4-byte length before sending.
        """
        # Packs the message with 4 leading bytes representing the message length
        msg = struct.pack('>I', len(msg)) + msg
        # Sends the packed message
        self.client_socket.send(msg)

    def _receive(self, sock):
        """
        Receives an incoming message from the client and unpacks it.

        :param sock: the incoming socket
        :return: the unpacked message
        """
        data = None
        # Retrieves the first 4 bytes from the message
        msg_len = sock.recv(self.RECV_MSG_LEN)
        # If the message has the 4 bytes representing the length...
        if msg_len:
            data = ''
            # Unpacks the message and gets the message length
            msg_len = struct.unpack('>I', msg_len)[0]
            # Computes the number of expected chunks of RECV_BUFFER size
            chunks = int(math.ceil(msg_len / float(self.RECV_BUFFER)))
            for _ in xrange(chunks):
                # Retrieves the chunk i-th chunk of RECV_BUFFER size
                chunk = sock.recv(self.RECV_BUFFER)
                # If there isn't the expected chunk...
                if not chunk:
                    data = None
                    break # ... Simply breaks the loop
                else:
                    # Merges the chunks content
                    data += chunk
        return data

    def _run(self):
        """
        Actually runs the client.
        """
        while self.running:
            socket_list = [sys.stdin, self.client_socket]

            # Gets the list of sockets which are ready to be read through select non-blocking calls
            # The select has a timeout of 60 seconds
            try:
                ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 60)
            except socket.error:
                continue
            else:
                for sock in ready_to_read:
                    # If there's an incoming message from the server...
                    if sock == self.client_socket:
                        data = self._receive(sock)  # Gets the server message
                        if not data:
                            print '\nDisconnected from the server.'
                            sys.exit()
                        else:
                            sys.stdout.write(data)  # Writes the server message
                            self._prompt()          # followed by a prompt
                    # ... else, the user has entered a message on the console
                    else :
                        msg = sys.stdin.readline()
                        self._send(msg) # Sends the message to the server...
                        self._prompt()  # ...and returns the prompt
        # Clears the socket connection
        self.stop()

    def run(self):
        """Given a host and a port, establishes the connections and runs the client.
        """
        self._connect()
        self._prompt()
        self._run()

    def stop(self):
        """
        Stops the client by setting the "running" flag to close before closing
        the socket connection.
        """
        self.running = False
        self.client_socket.close()

def main():
    """
    The main function of the program. It creates and runs a new ChatClient.
    """
    chat_client = ChatClient(_HOST, _PORT)
    chat_client.start()


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
