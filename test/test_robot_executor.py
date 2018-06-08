import unittest
import time
import socket
import multiprocessing
from mock import Mock

import RobotExecutor


class TestRobotExecutor(unittest.TestCase):
    def setUp(self):
        self.robot_executor = RobotExecutor.RobotExecutor()

    def test_parse_keyword_and_argument(self):
        output = self.robot_executor._parse("log    message")
        self.assertEqual([["log", "message"]], output)

    def test_parse_extra_spaces(self):
        output = self.robot_executor._parse("    log     message   ")
        self.assertEqual([["log", "message"]], output)

    def test_parse_newline(self):
        output = self.robot_executor._parse("    log     message \n  ")
        self.assertEqual([["log", "message"]], output)

    def test_parse_two_lines(self):
        output = self.robot_executor._parse(
            "   log    first\n   logtoconsole    second")
        self.assertEqual([["log", "first"], ["logtoconsole", "second"]],
                         output)

    def test_execute_tcp(self):
        self.robot_executor._run_line = Mock()
        p = multiprocessing.Process(target=self.robot_executor.execute_tcp)
        p.start()
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 10011))
        sock.send(b"Test Keyword")
        sock.close()
        time.sleep(1)
        p.terminate()
        p.join()

    def test_execute_tcp_exit(self):
        self.robot_executor._run_line = Mock()
        p = multiprocessing.Process(target=self.robot_executor.execute_tcp)
        p.start()
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 10011))
        sock.send(b"exit")
        sock.close()
        time.sleep(1)
        p.join()
