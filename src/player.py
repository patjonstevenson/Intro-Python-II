# Write a class to hold player information, e.g. what room they are in
# currently.

class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def drop_item(self, name):
        # Find item
        count = 0
        for i in self.inventory:
            if i.name == name:
                index = count
            count += 1
        return self.inventory.pop(index)

    def move(self, direction):
        next_room = getattr(self.current_room, f"{direction}_to")
        if next_room:
            self.current_room = next_room
        else:
            print(f"There is no room to the {direction}.")

