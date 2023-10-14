import json

import requests

class Website:
    preset_endpoint = 'https://ssrando.com/api/dynamicdata/racePresets'

    def __init__(self):
        self.presets = self.load_presets()

    def load_presets(self):
        presets = requests.get(self.preset_endpoint).json()

        preset_list = {}
        for array in presets:
            preset_list[array["data"]["settings"]] = array["data"]["name"]

        return preset_list