class ServerAllocator:
    """Class to allocate servers to users."""

    def __init__(self):
        """Initialize class variables."""
        self.input_file = None
        self.output_file = None

        self.tmax = None
        self.umax = None

        self.servers = None

        self.servers_cost = None

    def count_runnig_tasks(self, server_index):
        """Return the number of tasks running."""
        count_tasks = 0
        for number_of_tasks in self.servers[server_index]:
            count_tasks += number_of_tasks
        return count_tasks

    def add_in_the_last_server(self, number_of_users_add):
        """Add a fitting number of users on the last server."""
        self.servers[-1][self.tmax - 1] += number_of_users_add

    def add_users(self, number_users):
        """Add new users to servers."""
        while number_users > 0:
            if (len(self.servers) == 0 or
                    self.count_runnig_tasks(-1) == self.umax):
                self.servers.append(self.tmax * [0])
            number_of_users_add = min(
                number_users, self.umax - self.count_runnig_tasks(-1))
            self.add_in_the_last_server(number_of_users_add)
            number_users -= number_of_users_add

    def write_servers_to_file(self):
        """
        Write to the output file the servers
        with it's number of users.
        """
        if len(self.servers) == 0:
            self.output_file.write('0\n')
            return
        for i in range(len(self.servers)):
            self.output_file.write(str(self.count_runnig_tasks(
                i)) + (',' if i != (len(self.servers) - 1) else ''))
        self.output_file.write('\n')

    def tick(self):
        """Give a tick and update the server users."""
        for i in range(0, len(self.servers)):
            for j in range(1, self.tmax):
                self.servers[i][j - 1] = self.servers[i][j]
            self.servers[i][-1] = 0

        self.servers_cost += len(self.servers)

    def remove_empty_servers(self):
        """Remove the servers that are now empty of users."""
        while len(self.servers) > 0 and self.count_runnig_tasks(0) == 0:
            self.servers.pop(0)

    def init_allocation(self):
        """
        Read input file, allocate the servers to new users and
        write them with the total cost to output file.
        """
        self.input_file = open('input.txt', 'r')
        lines = self.input_file.readlines()

        self.output_file = open('output.txt', 'w')

        self.tmax = int(lines[0])
        self.umax = int(lines[1])

        self.servers = []

        self.servers_cost = 0

        for number_users in lines[2:]:
            self.add_users(int(number_users))
            self.write_servers_to_file()
            self.tick()

            self.remove_empty_servers()

        while len(self.servers) > 0:
            self.write_servers_to_file()
            self.tick()
            self.remove_empty_servers()

        self.output_file.write('0\n')
        self.output_file.write(str(self.servers_cost))

        self.input_file.close()
        self.output_file.close()


if __name__ == '__main__':
    server = ServerAllocator()
    server.init_allocation()
