############################################################################
# KeysBox Created By Matin Afzal
# https://github.com/MatinAfzal
# contact.matin@yahoo.com
############################################################################

from colorama import init, Fore
from os import system, path, listdir
from box import Box
from time import sleep
from columnar import columnar
from platform import system as ps
from datetime import datetime
from hashlib import md5
import json

# File identity information
__author__ = "Matin Afzal (contact.matin@yahoo.com)"
__version__ = "0.0.1"
__last_modification__ = "2023/08/09"

# Colorama init
init()
YELLOW = Fore.YELLOW
RESET = Fore.RESET

# running file path
dirname = path.dirname(__file__)

def login() -> None:
    """
    login page
    """
    while True:
        system('cls' or 'delete')
        banner()
        with open(os_valid_path(dirname, ["saves", "l1.txt"]),'r') as openfile:
                    first = json.load(openfile)
        if first[0] != 1:
            new_login_key = md5(input("Select password for your box: ").encode("utf-8")).hexdigest()
            first = [1, new_login_key]
            with open(os_valid_path(dirname, ["saves", "l1.txt"]), "w") as outfile:
                json.dump(first, outfile)
                print("Box Created successfully...")
                sleep(2)
        else:
            while True:
                system('cls' or 'delete')
                banner()
                login_password = md5(input("Enter the box password: ").encode("utf-8")).hexdigest()
                if first[1] == login_password:
                    break
                else:
                    print("Box password incorrect!")
                    sleep(2)
            break

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
    
# Box init
box = Box(os_valid_path(dirname, ["saves", "box.txt"]))

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
        2 : Import new password
        3 : Update & Delete passwords
        4 : Make backup
        5 : Exit""")

        command = input("--> ")
        validCommnads = ["1", "2", "3", "4", "5"]

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

        for key, val in box.box_dict().items():
            data.append([index, key, val[0], val[1]])
            index+=1

        headers = ["Number", "Title", "Password", "Caption"]
        table = columnar(data, headers)
        print(table)

        if justShow:
            any_key = input("Enter any key to menu...")

    else:
        print("there is no passwords!")
        sleep(2)

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

def terminal_backup() -> None:
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
        print(table)
    else:
        pass

    # make backups
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y--%H.%M.%S")
    path = os_valid_path(dirname, ["backups", f"{dt_string}.txt"])
    data = box.box_dict()
    save_backup(path, data)
    print("new backup created successfilly!")
    input("Enter any key to menu...")

def save_backup(path, data) -> None:
    """
    Save data in path.
    """
    try:
        with open(path, "w") as outfile:
            json.dump(data, outfile)
    except:
        print("there is a error during saving backup!")

if __name__ == "__main__":
    login()
    # Main Loop
    run = True
    while run:
        command = terminal_menu()
        if command == "1":
            terminal_show()
        elif command == "2":
            terminal_import()
        elif command == "3":
            terminal_update()
        elif command == "4":
            terminal_backup()
        elif command == "5":
            run = False
