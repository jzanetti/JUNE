from june.groups.group import Group, Supergroup
from june.logger_creation import logger
from enum import IntEnum


class Cemetery:
    def __init__(self):
        self.people = []
    #class GroupType(IntEnum):
    #    default = 0

    #def must_timestep(self):
    #    return False

    #def update_status_lists(self, time=1, delta_time=1):
    #    pass

    #def set_active_members(self):
    #    pass

    def add(self, person):
        self.people.append(person)


class Cemeteries(Supergroup):
    def __init__(self):
        super().__init__()
        self.members = [Cemetery()]

    def get_nearest(self, person):
        return self.members[0]
