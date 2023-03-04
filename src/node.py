class Node:
    """ Represents information about a node."""

    def __init__(self, ip_enum):
        self.ip = "192.168.1." + str(ip_enum)

    def __str__(self):
        return str(vars(self))

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if self.ip == other.ip:
            if (not hasattr(self, "region") and not hasattr(other,
                                                            "region") and not hasattr(
                self, "store")
                    and not hasattr(other, "store")):
                return True
            elif (hasattr(self, "region") and hasattr(other,
                                                      "region") and self.region == other.region and
                  hasattr(self, "store") and hasattr(other,
                                                     "store") and self.store == other.store):
                return True
            else:
                return False
        else:
            return False
