# Implement a class to hold room information. This should have name and
# description attributes.

from exceptions import ItemNotFound


class Room():
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_item(self, name):
        # Find item
        count = 0
        index = None
        for i in self.items:
            if i.name == name:
                index = count
            count += 1
        if index == None:
            raise ItemNotFound
        return self.items.pop(index)
