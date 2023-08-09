############################################################################
# KeysBox Created By Matin Afzal
# https://github.com/MatinAfzal
# contact.matin@yahoo.com
############################################################################

import json

# File identity information
__author__ = "Matin Afzal (contact.matin@yahoo.com)"
__version__ = "0.0.1"
__last_modification__ = "2023/09/8"

class Box():
    """
    The Box Of Keys
    """
    def __init__(self, path) -> None:
        self.path = path
        try:
            with open(self.path, 'r') as openfile:
                self.box = json.load(openfile)
        except:
            print("the is error during opening save files")

    def box_dict(self) -> dict:
        return self.box
    
    def box_update(self, dict) -> None:
        try:
            with open(self.path, "w") as outfile:
                json.dump(dict, outfile)
        except:
            print("there is a error during updating box")