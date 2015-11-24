"""
Created on 23/11/2015

@author: gioia

This script provides test cases for the socket-implementation of a simple chat sever-client application.

The code is organized as follows:
- the ChatServerTest class tests the ChatServer (defined in the chat_server module);
- the ChatClientTest class tests the ChatClient (defined in the chat_client module).

The programming language used is Python 2.7 and it is assumed you have it installed into your PC.
The operating system of reference is Linux. There are two basic ways to execute this script in Linux:
1 - launching it by the command shell through the python command;
2 - making it executable first and then launching it by the command shell.


Enjoy!
"""
import time
import socket
import unittest
import threading

from chat_server import ChatServer
from chat_client import ChatClient

_HOST = '127.0.0.1'  # defines the host as "localhost"
_PORT = 10000        # defines the port as "10000"
_RECV_BUFFER = 4096  # defines the size for the receiving buffer


class ChatServerTest(unittest.TestCase):
    """
    Provides tests for the ChatServer application.
    """

    HOST = _HOST
    PORT = _PORT
    RECV_BUFFER = _RECV_BUFFER

    def setUp(self):
        """
        Sets up the test environment by running a new ChatServer thread.
        """
        self.chat_server = ChatServer(self.HOST, self.PORT)
        self.chat_server.start()

        time.sleep(1)  # Gives the client the time for connecting to the server

    def _get_fake_client(self):
        """
        Returns a fake client.

        :return: a socket connected with the known (host, port) pair
        """
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect((self.HOST, self.PORT))
        return fake_client

    def test_connection(self):
        """
        Tests the client-server connection.
        """
        fake_client = self._get_fake_client()
        fake_client.close()

    def _get_enter_message(self, socket_name):
        """
        Given the pair (host, port), returns the message the server should broadcast
        to all the clients each time a new client connects.

        :param socket_name: the (host, port) pair related to the client connection
        :return: the message broadcast by the server when a new client connects
        """
        return "\n[%s:%s] entered the chat room\n" % socket_name

    def _get_broadcast_message(self, socket_name, msg):
        """
        Given the pair (host, port) and a message, returns the message the server should
        broadcast to all the clients.

        :param socket_name: the (host, port) pair related to the client connection
        :param msg: the message sent by the client
        :return: the message broadcast by the server
        """
        return "\r" + '<' + str(socket_name) + '> ' + msg

    def test_broadcast(self):
        """
        Tests the message broadcasting performed by the server.
        """
        fc1 = self._get_fake_client()  # The first client connects

        fc2 = self._get_fake_client()  # The second client connects
        fc2_enter_msg = self._get_enter_message(fc2.getsockname())
        self.assertEqual(fc1.recv(self.RECV_BUFFER), fc2_enter_msg)

        fc3 = self._get_fake_client()  # The third client connects
        fc3_enter_msg = self._get_enter_message(fc3.getsockname())
        self.assertEqual(fc1.recv(self.RECV_BUFFER), fc3_enter_msg)
        self.assertEqual(fc2.recv(self.RECV_BUFFER), fc3_enter_msg)

        fc3_orig_msg = 'Hello'
        fc3.send(fc3_orig_msg)  # The third client sends a message
        fc3_broadcast_msg = self._get_broadcast_message(fc3.getsockname(), fc3_orig_msg)
        self.assertEqual(fc1.recv(self.RECV_BUFFER), fc3_broadcast_msg)
        self.assertEqual(fc2.recv(self.RECV_BUFFER), fc3_broadcast_msg)

        fc1.close()
        fc2.close()
        fc3.close()

    def tearDown(self):
        """
        Clears the test environment by stopping the server.
        """
        time.sleep(1)  # Gives the client the time for disconnecting from the server
        self.chat_server.stop()


class ChatClientTest(unittest.TestCase):
    """
    Provides tests for the ChatClient application.
    """

    HOST = _HOST
    PORT = _PORT
    RECV_BUFFER = _RECV_BUFFER

    def _fake_server(self):
        """
        Simulates a server that listens for a connection and then closes it.
        """
        server_sock = socket.socket()
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Making the address reusable
        server_sock.bind((self.HOST, self.PORT))
        server_sock.listen(0)
        server_sock.accept()
        server_sock.close()

    def setUp(self):
        """
        Sets up the test environment by running a fake server in a background thread.
        """
        self.server_thread = threading.Thread(target=self._fake_server)
        self.server_thread.start()

    def test_connection(self):
        """
        Tests the client-server connection.
        """
        chat_client = ChatClient(self.HOST, self.PORT)
        chat_client.start()
        time.sleep(1)
        chat_client.stop()

    def tearDown(self):
        """
        Clears the test environment by ensuring the server will stop.
        """
        self.server_thread.join()


if __name__ == '__main__':
    """The entry point of the program. It simply runs the test cases.
    """
    unittest.main()
