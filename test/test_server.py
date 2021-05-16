import sys
sys.path.append("../code")
import unittest
from server_allocator import ServerAllocator


class BasicTestCase(unittest.TestCase):
    """Test case of a basic new input."""

    def setUp(self):
        """
        Start test case by reading input file and initializing
        ServerAllocator variables.
        """
        self.input_file = open('test_input.txt', 'r')
        self.test_case = self.input_file.readlines()

        self.server_allocator = ServerAllocator()
        self.server_allocator.tmax = int(self.test_case[0])
        self.server_allocator.umax = int(self.test_case[1])
        self.server_allocator.servers = [self.server_allocator.tmax * [0]]
        self.server_allocator.servers_cost = 0

    def tearDown(self):
        """Finish test case by closing input file."""
        self.input_file.close()

    def testBasic(self):
        """Test case with input [3, 3, 10, 8]."""
        """Add 10 new users, allocate 3 servers, give a tick and try to remove
           empty servers."""
        self.server_allocator.add_users(int(self.test_case[2]))
        assert self.server_allocator.servers == [[0, 0, 3], [0, 0, 3],
                                                 [0, 0, 3], [0, 0, 1]]

        self.server_allocator.tick()
        assert self.server_allocator.servers == [[0, 3, 0], [0, 3, 0],
                                                 [0, 3, 0], [0, 1, 0]]
        assert self.server_allocator.servers_cost == 4

        self.server_allocator.remove_empty_servers()
        assert self.server_allocator.servers == [[0, 3, 0], [0, 3, 0],
                                                 [0, 3, 0], [0, 1, 0]]

        """Add 8 new users, allocate 3 new servers, give a tick and try to
           remove empty servers."""
        self.server_allocator.add_users(int(self.test_case[3]))
        assert self.server_allocator.servers == [[0, 3, 0], [0, 3, 0],
                                                 [0, 3, 0], [0, 1, 2],
                                                 [0, 0, 3], [0, 0, 3]]

        self.server_allocator.tick()
        assert self.server_allocator.servers == [[3, 0, 0], [3, 0, 0],
                                                 [3, 0, 0], [1, 2, 0],
                                                 [0, 3, 0], [0, 3, 0]]
        assert self.server_allocator.servers_cost == 10

        self.server_allocator.remove_empty_servers()
        assert self.server_allocator.servers == [[3, 0, 0], [3, 0, 0],
                                                 [3, 0, 0], [1, 2, 0],
                                                 [0, 3, 0], [0, 3, 0]]

        """Give a tick and remove 3 empty servers."""
        self.server_allocator.tick()
        assert self.server_allocator.servers == [[0, 0, 0], [0, 0, 0],
                                                 [0, 0, 0], [2, 0, 0],
                                                 [3, 0, 0], [3, 0, 0]]
        assert self.server_allocator.servers_cost == 16

        self.server_allocator.remove_empty_servers()
        assert self.server_allocator.servers == [[2, 0, 0], [3, 0, 0],
                                                 [3, 0, 0]]

        """Give a tick and remove more 3 empty servers."""
        self.server_allocator.tick()
        assert self.server_allocator.servers == [[0, 0, 0], [0, 0, 0],
                                                 [0, 0, 0]]
        assert self.server_allocator.servers_cost == 19

        self.server_allocator.remove_empty_servers()
        assert self.server_allocator.servers == []


if __name__ == "__main__":
    unittest.main()
