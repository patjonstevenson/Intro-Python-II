from room import Room
from player import Player
from item import Item
from exceptions import EndGame, InputError, ItemNotFound

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

# Items
items = {
    'sword': Item('sword', 'two-handed melee weapon'),
    'grail': Item('grail', 'sanctum calicem - Domine non sum dignus...'),
    'breviary': Item('breviary', 'book containing the prayers of the Liturgy of the Hours')
}


#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

moves = ['n', 's', 'e', 'w', 'q']

'''
def make_a_move(room, direction):
    next_room = getattr(room, f"{direction}_to")
    return next_room or 0

def take_action(verb, obj):
    pass
'''


def initialize_rooms(rooms, items):
    rooms['outside'].add_item(items['sword'])
    rooms['foyer'].add_item(items['breviary'])
    rooms['treasure'].add_item(items['grail'])


def print_items(room):
    for item in room.items:
        print(f'Name: {item.name}')
        print(f'Description: {item.description}\n')


def handle_cmd(cmd, player):
    room = player.current_room
    directions = ['n', 's', 'e', 'w']
    verbs = ['get', 'take', 'drop']
    objects = room.items + player.inventory

    if " " not in cmd:
        if cmd == 'q':
            raise EndGame
        elif cmd in directions:
            player.move(cmd)
        elif cmd == 'i' or cmd == 'inventory':
            print("\nInventory:")
            for item in player.inventory:
                print(f'+ {item.name} +')
                print(f'"{item.description}"\n')
        else:
            print(f'"{cmd}" is not a valid move.')
    else:
        [verb, obj] = cmd.split(" ")
        if verb in verbs and obj in [obj.name for obj in objects]:
            try:
                if verb == "take" or verb == "get":
                    item = room.get_item(obj)
                    player.add_item(item)
                    print(f'You have picked up {obj}!')
                elif verb == "drop":
                    item = player.drop_item(obj)
                    room.add_item(item)
                    print(f'You have dropped {obj}!')
            except ItemNotFound:
                print(f'{obj} not found there!')

        else:
            raise InputError


def player_won(player):
    inventory = [item.name for item in player.inventory]
    room = player.current_room.name
    return 'grail' in inventory and room == 'Outside Cave Entrance'


def main():
    # Initialize player
    name = input("Enter your name: ")
    player = Player(name, room['outside'])
    print(f'Welcome to the game {name}!')

    # Initialize Rooms
    initialize_rooms(room, items)

    # Main loop
    try:
        while True:
            if player_won(player):
                print("You won!")
                raise EndGame
            print(f'\nCurrent location: {player.current_room.name}.')
            print(player.current_room.description)
            print('\nItems available in this room:\n')
            print_items(player.current_room)

            # Get player input
            # cmd = input("Which direction will you choose? ")
            cmd = input('~~> ')

            try:
                handle_cmd(cmd, player)
            except InputError:
                print(f'"{cmd}" is not a valid command.')

                # Validate input
                # if cmd not in moves:
                #     print(f'"{cmd}" is not a valid move. Please enter "n", "s", "e", "w", or "q"')
                #     continue

                # # Allow player to leave the game if they really want to
                # elif cmd == 'q':
                #     break

                # # Try to make a move.
                # # If that move leads to a room, set their current_room to that room.
                # # If that move doesn't lead to a room, let them know and restart the loop.
                # elif cmd in moves:
                #     #new_room = make_a_move(player.current_room, cmd)
                #     # if new_room:
                #     #    player.current_room = new_room
                #     # else:
                #     #    print("There is no room in that direction! Please try again.")
                #     player.move(cmd)

                # elif len(cmd) == 2:
                #     verb = cmd[0]
                #     obj = cmd[1]
    except EndGame:
        print(f"\nThank you for playing {player.name}!\n")
        pass


if __name__ == "__main__":
    main()
