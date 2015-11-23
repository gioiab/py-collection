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
import socket
import select
import threading

_HOST = '127.0.0.1'  # defines the host as "localhost"
_PORT = 10000        # defines the port as "10000"

class ChatClient(threading.Thread):

    RECV_BUFFER = 4096

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
                        data = sock.recv(4096)  # Gets the server message
                        if not data:
                            print '\nDisconnected from the server.'
                            sys.exit()
                        else:
                            sys.stdout.write('\n' + data)  # Writes the server message
                            self._prompt()                 # followed by a prompt
                    # ... else, the user has entered a message on the console
                    else :
                        msg = sys.stdin.readline()
                        self.client_socket.send(msg)
                        self._prompt()
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
