import random

class Draft:

    OPTIONS = {
        "3D Standard": "",
        "3D EUD Off": "",
        "2D EUD Off": "",
        "2D Cubes": "",
        "2D Keysanity": "",
        "2D Swordless": "",
        "2D Sky Keep": "",
        "3D Open": "",
        "3D Closed": "",
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
        self.banned.append(option)
        return f"Banned {option}"


    def make_selection(self):
        possible_selections = self.picked
        possible_selections.append(random.choice([
            option for option in self.OPTIONS
            if option not in self.banned and option not in self.picked
        ]))
        return self.OPTIONS[random.choice(possible_selections)]

