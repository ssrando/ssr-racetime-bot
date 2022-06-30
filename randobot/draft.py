import random


class Draft:

    OPTIONS = {
        "3D Standard": "oQ0AIDADo5oJUgAAAAAAAAAYFA==",
        "3D EUD Off": "oQUAIDADo5oJUgAAAAAAAAAcGA==",
        "2D Cubes": "IQ0AIBADo5oJUgAAAAAAAAAYEA==",
        "3D Keysanity": "oQ0AIDADo5oJmgAAAAAAAAAYFA==",
        "3D Swordless": "gQ0AIDADo5oJUgAAAAAAAAAcFA==",
        "3D Open": "pw0AIDADo5oJUgAAAAAAAAAYFA==",
    }

    def __init__(self) -> None:
        self.all_options = self.OPTIONS.keys()
        self.banned = []
        self.picked = []
        self.spoiler_log = True
        self.high_seed = ""
        self.low_seed = ""
        self.guide_step = None

    def ban(self, option):
        if (self.guide_step is not None) and (self.guide_step % 2 == 1):
            # the current step in the guide expects a player to pick an option
            return "Currently, a player should be picking an option, not banning one."
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
        return_string = f"Banned {option}"
        if self.guide_step == 0:
            return_string += f". {self.high_seed}, please pick an option."
            self.guide_step += 1
        elif self.guide_step == 2:
            return_string += f". {self.low_seed}, please pick an option."
            self.guide_step += 1
        return return_string

    def pick(self, option):
        if (self.guide_step is not None) and (self.guide_step % 2 == 0):
            # the current step in the guide expects a player to ban an option
            return "Currently, a player should be banning an option, not picking one."
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
        return_string = f"Picked {option}"
        if self.guide_step == 1:
            return_string += f". {self.high_seed}, please ban an option."
            self.guide_step += 1
        elif self.guide_step == 3:
            return_string += f". When everyone is ready, have someone use !rollseed to roll the seed. I will choose one unbanned option to add to the pool as well, and then select one option from the pool."
        return return_string

    def set_log_state(self, option):
        if option == "off":
            self.spoiler_log = False
            return "Spoiler log generation is now turned OFF."
        elif option == "on":
            self.spoiler_log = True
            return "Spoiler log generation is now turned ON."
        else:
            return "Invalid argument. Please specify 'off' to turn off the spoiler log or 'on' to turn it on."

    def seeding_init(self, high_seed, low_seed):
        self.high_seed, self.low_seed = high_seed, low_seed
        self.guide_step = 0
        return f"Draft guide has been enabled. Note that this means picks and bans will only go through if chosen in the correct order. Please disable guide mode to fully unlock. {self.high_seed}, you have been set as the higher seed, and {self.low_seed}, you have been set as the lower seed. {self.low_seed}, please ban an option."

    def make_selection(self):
        possible_selections = self.picked
        possible_selections.append(
            random.choice(
                [
                    option
                    for option in self.OPTIONS
                    if option not in self.banned and option not in self.picked
                ]
            )
        )
        choice = random.choice(possible_selections)
        perma = self.OPTIONS[choice]
        # the ninth character of every permalink in the draft options is 'o' when spoiler log if on, but '4' when spoiler log if off
        if not self.spoiler_log:
            perma = ""
            for n, c in enumerate(self.OPTIONS[choice]):
                if n == 8:
                    perma += "4"
                else:
                    perma += c
        return (choice, perma)
