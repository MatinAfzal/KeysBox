import os

from colorama import init, Fore
from os import system, path, listdir
from cryptography.fernet import Fernet
from box import Box
from time import sleep
from columnar import columnar
from platform import system as ps
from datetime import datetime
from hashlib import md5
import json
import shutil

# File identity information
__author__ = "Matin Afzal (contact.matin@yahoo.com)"
__version__ = "1.2.0"

# 1.0.0 -> initial version.
# 1.1.0 -> fernet encryption feature.
# 1.2.0 -> password search feature.
# TODO 1.3.0 -> Signatures & Documents storing.

# Colorama init
init()
YELLOW = Fore.YELLOW
RESET = Fore.RESET

# running file path
dirname = path.dirname(__file__)


def login(inital=None):
    """
    login page
    """
    first_flag = False
    while True:
        system('cls' or 'delete')
        banner()

        with open(os_valid_path(dirname, ["saves", "l1.txt"]), 'r') as openfile:
            first = json.load(openfile)

        if first[0] != 1:
            new_login_key = md5(input("Select password for your box: ").encode("utf-8")).hexdigest()
            fernet_login_key = Fernet.generate_key()
            temp_flk = md5(fernet_login_key).hexdigest()
            first = [1, new_login_key, temp_flk]

            with open(os_valid_path(dirname, ["saves", "l1.txt"]), "w") as outfile:
                json.dump(first, outfile)
                print("Box Created successfully...")
                outfile.close()
                sleep(2)

            with open('loginKey.key', 'wb') as filekey:
                filekey.write(fernet_login_key)
                filekey.close()

            with open('loginKey.key', 'rb') as filekey:
                return_key = filekey.read()

            data_path = os_valid_path(dirname, ["saves", "box.txt"])
            init_dict = {}
            with open(data_path, 'w') as openfile:
                json.dump(init_dict, openfile)

            first_flag = True

            print("your private loginKey.key created! (RUN THE PROGRAM AGAIN)\n"
                  "Note: save your login key in safe place! ")
            sleep(2)

            return first_flag, return_key
        else:
            while True:
                system('cls' or 'delete')
                banner()
                login_password = md5(input("Enter the box password: ").encode("utf-8")).hexdigest()
                if first[1] == login_password:
                    fernet_login_key_path = input("Enter path to your login key path: ")
                    with open(fernet_login_key_path, 'rb') as filekey:
                        return_key = filekey.read()
                    encrypted = md5(return_key).hexdigest()

                    if encrypted == first[2]:
                        return first_flag, return_key
                    else:
                        print("Fernet Key not match to initial key!")
                        sleep(2)
                else:
                    print("Box password incorrect!")
                    sleep(2)


def os_valid_path(dirname, paths) -> str:
    """
    Configure the correct path based on the operating system.
    """
    os = ps()
    if os == "Windows" or os == "Darwin":
        for path in paths:
            dirname += f"\\{path}"
        return dirname
    else:
        for path in paths:
            dirname += f"/{path}"
        return dirname


def banner() -> None:
    """
    Display keys box banner.
    """
    print(YELLOW+"""
             ,╓╦@@@@@m╖,
          ╓@╢▒▒╢╢╢╢╢╢╜░░░▒,
        g╣▒╢╜░▄╩╜"``"`▒░░░░▒┐
      ╓▓▒╢░▄▀           ▒╢╢▒▒L
     ╓▒▒╢░▓              ╢▒▒▒▓
     ╢▒▒░▓               ╢▒▒░▓
    ]▒▒▒▒               ╓▒▒╢░▓
     ▒▒╢░L             ╓╢▒╢░▓
     ╟░░░▒,          ╓╬║╙╙░▀
      ╙░░░░▒@╥╖╖╓╦@╬▒▒▓▓╢╖░,▒▒╗
        ▒▒╢╢▒▒▒▒▒╢╢╜▒░▓▓▓▓╢╖░ä╜╖
          `╙╧Ñ▒W@Å╩╨"  ╚▓▓▓▓▓╖   h
                         ▀'▀▓▓▓@   ░,
                             ╙▓▓▓╢,  ░,
                               ╙▓▓▓╢╖  ░╖
                                 "▓▓▓╢╖░▒░░N
                                    ▓▓▓▒╢░╜ »
                                    ╙▓▓▓▓▒@,  ░,
                                      `╓▒▓▓▓╢,  ░,
                                     ╒▓░╙╢▒▓▓▓╢╖  ░╖
                                      ╣╢░░╜╢▒▒▓▓╢╖  ░╕
                                ,φ╗,@▒╣╜ ▀▓░░╢▒▒▓▓╣╗,`
                                 ╙▓▒╨`   ,╣╢▒░░╝╙▀▀`
                                   '   ╓▓▒Ñ` ╙
                                      ▓@╙╗
            Created by Matin Afzal
                github: https://github.com/MatinAfzal
"""+RESET)


def terminal_menu() -> str:
    """
    Display keys box main menu.
    """
    while True:
        system('cls' or 'clear')
        banner()
        print("""
        1 : Display passwords
        2 : Signatures & Documents
        3 : Import new password
        4 : Update & Delete passwords
        5 : Take Backup
        6 : Exit""")

        command = input("--> ")
        validCommnads = ["1", "2", "3", "4", "5", "6"]

        if command not in validCommnads:
            print("wrong command!")
            sleep(2)
            continue

        return command


def terminal_import() -> None:
    """
    Import the new password to keysbox.
    """
    while True:
        title = input("select title for your password: ")
        box_dict = box.box_dict()

        if title in box_dict:
            print("this password title already exist!\nselect unique one!")
            continue
        password = input(f"enter [{title}] password: ")
        caption = input(f"enter [{title}] caption: ")

        try:
            box_dict[title] = [password, caption]
            box.box_update(box_dict)
        except:
            print("There is an error during importing new password!")
            exit()
        else:
            print("password saved successfully!")
            sleep(2)
            break


def terminal_show(justShow=True) -> None:
    """
    Display passwords.
    """
    system('cls' or 'clear')
    banner()

    if len(box.box_dict()) != 0:
        data = []
        index = 0
        index_key = []
        for key, val in box.box_dict().items():
            data.append([index, key, val[0], val[1]])
            index_key.append([index, key])
            index += 1

        headers = ["Number", "Title", "Password", "Caption"]
        table = columnar(data, headers)
        print(table)

        if justShow:
            any_key = input("Enter any key to menu or [-1] to search: ")
            if any_key == "-1":
                os.system("cls" or "clear")
                banner()

                search_result = []
                search_filtered_data = []
                searched_key = input("Enter any letter of tittle to search: ")
                letters = set(searched_key)
                print("Founded Information's: ")
                for index, key in index_key:
                    if letters & set(key):
                        search_result.append(index)

                for index, key, val0, val1 in data:
                    if index in search_result:
                        search_filtered_data.append([index, key, val0, val1])

                headers = ["Number", "Title", "Password", "Caption"]
                table = columnar(search_filtered_data, headers)
                print(table)

                option = input("Enter any key to return or [-1] to menu: ")
                if option != "-1":
                    terminal_show(justShow=True)



    else:
        print("there is no passwords!")
        sleep(2)


def terminal_sign_and_docs():
    os.system("cls" or "clear")
    banner()

    print("""
        1 : Display Documents
        2 : Import Documents
        3 : Return
        """)

    option = input("-->")
    print("Not available!")



def terminal_update() -> None:
    """
    Update and delete passwords menu.
    """
    while True:
        if len(box.box_dict()) == 0:
            print("there is no passwords!")
            sleep(2)
            break

        terminal_show(False)
        number = int(input("Select password number to edit or [-1 to return menu]: "))

        if number == -1:
            break
        elif number > len(box.box_dict()) - 1:
            print("selected number out of range!")
            continue

        system('cls' or 'clear')
        banner()

        # Processing passwords to display in table format.
        box_dict = box.box_dict()
        headers = ["Number", "Title", "Password", "Caption"]
        data = list(box_dict.items())[number]
        data = [[number, data[0], data[1][0], data[1][1]]]
        table = columnar(data, headers)
        print(table)
        
        while True:
            system('cls' or 'clear')
            banner()

            headers = ["Number", "Title", "Password", "Caption"]
            data = list(box_dict.items())[number]
            data = [[number, data[0], data[1][0], data[1][1]]]
            table = columnar(data, headers)
            print(table)

            print("""
            1 : Change password
            2 : Edit caption
            3 : Delete password
            4 : Return
            """)

            box_dict = box.box_dict()
            data = list(box_dict.items())[number]
            valid = ["1", "2", "3", "4"]
            command = input("--> ")

            if command not in valid:
                continue
            # Change password.
            elif command == "1":
                new_pass = input(f"Enter new password for {data[0]}: ")
                box_dict[data[0]] = [new_pass, data[1][1]]
                box.box_update(box_dict)
                continue
            # Change caption
            elif command == "2":
                new_caption = input(f"Enter new caption for {data[0]}: ")
                box_dict[data[0]] = [data[1][0], new_caption]
                box.box_update(box_dict)
                continue
            # Delete password
            elif command == "3":
                command = input(f"Are you sure to delete {data[0]}? [Y/N]: ").lower()
                if command == "y" or "yes":
                    del box_dict[data[0]]
                    box.box_update(box_dict)
                    print("Password deleted successfully!")
                    sleep(2)
                    break

            elif command == "4":
                break      


def terminal_backup(key) -> None:
    """
    Display backups and make new backup.
    """
    # display backups
    backs = []
    backups = listdir(os_valid_path(dirname, ["backups"]))
    if backups:
        for backup in backups:
            backs.append([backup])
        header = ["Backup name"]
        table = columnar(backs, header)
    else:
        table = "ERROR!"
        pass

    # make backups
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y--%H.%M.%S")
    path = os_valid_path(dirname, ["backups", f"{dt_string}.txt"])
    data_path = os_valid_path(dirname, ["saves", "box.txt"])
    save_backup(path, data_path, key)
    print("new backup created successfilly!")
    print(table)
    input("Enter any key to menu...")


def save_backup(path, data_path, key) -> None:
    """
    Save data in path.
    """
    shutil.copyfile(data_path, path)


if __name__ == "__main__":
    first_run, key = login()

    # Box init
    box = Box(os_valid_path(dirname, ["saves", "box.txt"]), key=key, first=first_run)

    # Main Loop
    if not first_run:
        run = True
        while run:
            command = terminal_menu()
            if command == "1":
                terminal_show()
            elif command == "2":
                terminal_sign_and_docs()
            elif command == "3":
                terminal_import()
            elif command == "4":
                terminal_update()
            elif command == "5":
                terminal_backup(key)
            elif command == "6":
                run = False

        # make backups
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y--%H.%M.%S")
        path = os_valid_path(dirname, ["backups", f"{dt_string}.txt"])
        data_path = os_valid_path(dirname, ["saves", "box.txt"])
        save_backup(path, data_path, key)

        box.box_decrypt()
        box.box_encrypt()
