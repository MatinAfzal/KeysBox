############################################################################
# KeysBox Created By Matin Afzal
# https://github.com/MatinAfzal
# contact.matin@yahoo.com
############################################################################

import json
from cryptography.fernet import Fernet

# File identity information
__author__ = "Matin Afzal (contact.matin@yahoo.com)"
__version__ = "0.0.1"
__last_modification__ = "2023/08/09"

class Box:
    """
    The Box Of Keys
    """
    def __init__(self, path, key=None, first=False) -> None:
        self.path = path
        self.key = key
        self.temp = None

        if first:
            self.box_encrypt()
        # self.box_decrypt()
        #
        # with open(self.path, 'r') as openfile:
        #     temp = json.load(openfile)
        #
        # self.box_encrypt()

        self.box = self.box_dict()

    def box_dict(self):
        self.box_decrypt()
        self.box = self.read_normaly()
        self.box_encrypt()
        return self.box
    
    def box_update(self, dict) -> None:
        self.box_decrypt()

        with open(self.path, "w") as outfile:
            json.dump(dict, outfile)

        self.box_encrypt()

    def box_encrypt(self):  # Locking
        with open(self.path, 'rb') as enc_file:
            encrypted = enc_file.read()
            enc_file.close()

        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(encrypted)

        with open(self.path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            encrypted_file.close()

    def box_decrypt(self):  # Unlocking
        with open(self.path, 'rb') as enc_file:
            encrypted = enc_file.read()
            enc_file.close()

        fernet = Fernet(self.key)
        data = fernet.decrypt(encrypted)

        with open(self.path, 'wb') as dec_file:
            dec_file.write(data)
            dec_file.close()

        self.box = self.read_normaly()

    def read_normaly(self):
        with open(self.path, 'r') as openfile:
            temp = json.load(openfile)
        return temp
