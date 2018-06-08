import socket
import re

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class RobotExecutor(object):
    """Library for executing robot framework commands from wanted source.

    Before executing anything the incoming message is parsed. So one can for
    example send a message where there are extra whitespaces.

    There is a special command called 'exit' which stops the keyword and
    continues the traditional execution.
    """

    def execute_tcp(self, host='127.0.0.1', port=10011):
        """Execute commands sent TCP port.

        Parameters
        ----------
        host : string
            Host name or ip address.
        port : int
            Port that is listened.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))  # Bind the socket to the port
        sock.listen(1)  # Listen for incoming connections
        while True:
            # Wait for a connection
            logger.info('\nListening for commands..', also_console=True)
            connection, client_address = sock.accept()
            try:
                data = ""
                while True:
                    chunk = connection.recv(1024)
                    if chunk:
                        data += chunk
                    else:
                        break
            finally:
                connection.close()  # close the connection
                lines = self._parse(data)
                for line in lines:
                    self._run_line(line)
                if lines[0][0] == 'exit':
                    sock.close()
                    return

    def _run_line(self, line):
        logger.info("> {}".format("  ".join(line)), also_console=True)
        try:
            result = BuiltIn().run_keyword(*line)
        except Exception as result:
            pass
        logger.info("< {}".format(result), also_console=True)

    def _parse(self, data):
        data = data.strip()
        lines = data.split("\n")
        keyword_separator = re.compile('  +| ?\t+ ?')
        return [keyword_separator.split(line.strip()) for line in lines]
