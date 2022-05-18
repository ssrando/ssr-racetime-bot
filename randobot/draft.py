import random

class Draft:

    OPTIONS = {
        "3D Standard": "",
        "3D EUD Off": "oQUAIDADo5oJUgAAAAAAAAAcBA==",
        "2D EUD Off": "IQUAIDADo5oJUgAAAAAAAAAYBA==",
        "2D Cubes": "IQ0AIBADo5oJUgAAAAAAAAAYBA==",
        "2D Small Keysanity": "IQ0AIDADo5oJWgAAAAAAAAAYBA==",
        "2D Full Keysanity": "IQ0AIDADo5oJmgAAAAAAAAAYBA==",
        "2D Swordless": "gQ0AIDADo5oJUgAAAAAAAAAcBA==",
        "2D Sky Keep": "IQ0AIDADopoJUgAAAAAAAAAYBA==",
        "3D Open": "pw0AIDADo5oJUgAAAAAAAAAYBA==",
        "3D Closed": "oA0AIDADo5oBUgAAAAAAAAAQBA==",
    }

    def __init__(self) -> None:
        self.all_options = self.OPTIONS.keys()
        self.banned = []
        self.picked = []


    def ban(self, option):
        if option in self.banned:
            # option cannot be banned twice
            return f"Unable to ban option {option} - it has already been banned"
        if option in self.picked:
            # option cannot be banned once picked
            return f"Unable to ban option {option} - it has already been picked"
        if option not in self.all_options:
            # invalid choice
            return f"Unable to ban option {option} - invalid option"
        self.banned.append(option)
        return f"Banned {option}"

    
    def pick(self, option):
        if option in self.banned:
            # option cannot be picked if banned
            return f"Unable to pick option {option} - it has already been banned"
        if option in self.picked:
            # option cannot be picked twice
            return f"Unable to pick option {option} - it has already been picked"
        if option not in self.all_options:
            # invalid choice
            return f"Unable to pick option {option} - invalid option"
        self.picked.append(option)
        return f"Picked {option}"


    def make_selection(self):
        possible_selections = self.picked
        possible_selections.append(random.choice([
            option for option in self.OPTIONS
            if option not in self.banned and option not in self.picked
        ]))
        choice = random.choice(possible_selections)
        return (choice, self.OPTIONS[choice])

