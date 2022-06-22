import random

class Draft:

    OPTIONS = {
        "3D Standard": "oQ0AIDADo5oJUgAAAAAAAAAYBA==",
        "3D EUD Off": "oQUAIDADo5oJUgAAAAAAAAAcBA==",
        "2D Cubes": "IQ0AIBADo5oJUgAAAAAAAAAYBA==",
        "3D Keysanity": "oQ0AIDADo5oJmgAAAAAAAAAYBA==",
        "3D Swordless": "gQ0AIDADo5oJUgAAAAAAAAAcBA==",
        "3D Open": "pw0AIDADo5oJUgAAAAAAAAAYBA==",
    }

    def __init__(self) -> None:
        self.all_options = self.OPTIONS.keys()
        self.banned = []
        self.picked = []
        self.spoiler_log = True


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

    def set_log_state(self, option):
        if option == "off":
            self.spoiler_log = False
            return "Spoiler log generation is now turned OFF."
        elif option == "on":
            self.spoiler_log = True
            return "Spoiler log generation is now turned ON."
        else:
            return "Invalid argument. Please specify 'off' to turn off the spoiler log or 'on' to turn it on."


    def make_selection(self):
        possible_selections = self.picked
        possible_selections.append(random.choice([
            option for option in self.OPTIONS
            if option not in self.banned and option not in self.picked
        ]))
        choice = random.choice(possible_selections)
        perma = self.OPTIONS[choice]
        # the ninth character of every permalink in the draft options is 'o' when spoiler log if on, but '4' when spoiler log if off
        if not self.spoiler_log:
            perma = ""
            for n,c in enumerate(self.OPTIONS[choice]):
                if n == 8:
                    perma += "4"
                else:
                    perma += c
        return (choice, perma)

