"""
Created on 23/11/2015

@author: gioia

This script runs a simple ChatServer built with sockets.

The code is organized as follows:
- the ChatServer class defines the behaviour of the server;
- the main module function simply executes the server.

The programming language used is Python 2.7 and it is assumed you have it installed into your PC.
The operating system of reference is Linux. There are two basic ways to execute this script in Linux:
1 - launching it by the command shell through the python command;
2 - making it executable first and then launching it by the command shell.


Enjoy!
"""
import socket
import select
import threading

_HOST = '127.0.0.1'  # defines the host as "localhost"
_PORT = 10000        # defines the port as "10000"

class ChatServer(threading.Thread):
    """
    Defines the chat server as a Thread.
    """

    MAX_WAITING_CONNECTIONS = 10  # defines the max number of accepted waiting connections before the rejection
    RECV_BUFFER = 4096  # defines the size for the receiving buffer

    def __init__(self, host, port):
        """
        Initializes a new ChatServer.

        :param host: the host on which the server is bounded
        :param port: the port on which the server is bounded
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.connections = []  # collects all the incoming connections
        self.running = True  # tells whether the server should run

    def _bind_socket(self):
        """
        Creates the server socket and binds it to the given host and port.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.MAX_WAITING_CONNECTIONS)
        self.connections.append(self.server_socket)

    def _broadcast(self, client_socket, client_message):
        """
        Broadcasts a message to all the clients different from both the server itself and
        the client sending the message.

        :param client_socket: the socket of the client sending the message
        :param client_message: the message to broadcast
        """
        for sock in self.connections:
            is_not_the_server = sock != self.server_socket
            is_not_the_client_sending = sock != client_socket
            if is_not_the_server and is_not_the_client_sending:
                try :
                    sock.send(client_message)
                except socket.error:
                    # Handles a possible disconnection of the client "sock" by...
                    sock.close()  # closing the socket connection
                    self.connections.remove(sock)  # removing the socket from the active connections list

    def _run(self):
        """
        Actually runs the server.
        """
        while self.running:
            # Gets the list sockets which are ready to be read through select non-blocking calls
            # The select has a timeout of 60 seconds
            ready_to_read, ready_to_write, in_error = select.select(self.connections, [], [], 60)
            for sock in ready_to_read:
                # If the socket instance is the server socket...
                if sock == self.server_socket:
                    try:
                        # Handles a new client connection
                        client_socket, client_address = self.server_socket.accept()
                    except socket.error:
                        break
                    else:
                        self.connections.append(client_socket)
                        print "Client (%s, %s) connected" % client_address

                        # Notifies all the connected clients a new one has entered
                        self._broadcast(client_socket, "\n[%s:%s] entered the room\n" % client_address)
                # ...else is an incoming client socket connection
                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER) # Gets the client message...
                        if data:
                            # ... and broadcasts it to all the connected clients
                            self._broadcast(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                    except socket.error:
                        # Broadcasts all the connected clients that a clients has left
                        self._broadcast(sock, "\nClient (%s, %s) is offline\n" % client_address)
                        print "Client (%s, %s) is offline" % client_address
                        sock.close()
                        self.connections.remove(sock)
                        continue
        # Clears the socket connection
        self.stop()

    def run(self):
        """Given a host and a port, binds the socket and runs the server.
        """
        self._bind_socket()
        self._run()

    def stop(self):
        """
        Stops the server by setting the "running" flag to close before closing
        the socket connection.
        """
        self.running = False
        self.server_socket.close()


def main():
    """
    The main function of the program. It creates and runs a new ChatServer.
    """
    chat_server = ChatServer(_HOST, _PORT)
    chat_server.start()


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
    main()
