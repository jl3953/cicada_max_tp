class Node:
    """ Represents information about a node."""

    def __init__(self, ip_enum):
        self.ip = "192.168.1." + str(ip_enum)

    def __str__(self):
        return str(vars(self))

    def __hash__(self):
        return hash(self.ip)
