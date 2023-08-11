import os
import socket
import hashlib
import argparse
import threading


def password_cracker():
    print("**************PASSWORD CRACKER ******************")
    pass_found = 0  # To check if the password  found or not
    input_hash = input("Enter the hashed password: ")
    directory = str(input("Enter the directory where the hashed password will be stored: "))
    options = []
    for doc in os.listdir(directory):
        new = directory + doc
        if os.access(new, os.R_OK) is True:
            options.append(new)
        else:
            continue
    for pass_doc in options:
        try:
            pass_file = open(pass_doc, 'r')
            # comparing the input_hash with the hashes of the words in password file
            for word in pass_file:
                enc_word = word.encode('utf-8')
                hash_word = hashlib.md5(enc_word.strip())
                # digesting that hash into a hexadecimal value
                digest = hash_word.hexdigest()
                if digest == input_hash:
                    print(f"Password found.\nThe password is: {word}") # comparing hashes
                    pass_found = 1
                    break

            if not pass_found:
                print(f"Password is not found in the {pass_doc} file")
                print('\n')

            print("*****************  Thank you  **********************")
        except Exception as error:
            print(error)


def connection_scan():
    target_ip = input("Please provide the IP Address: ")
    target_port = [20, 21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 8080, 8181, 318]
    for port in target_port:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, port))
            s.send(b'Banner query\r\n')
            results = s.recv(100)
            print("[+] {}/tcp open".format(port))
            print("[+] {}".format(str(results)))
        except OSError:
            print("[-] {}/tcp closed".format(port))


def port_scan():
    target = input("Enter the target: ")
    port_num = [20, 21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 8080, 8181, 318]
    for x in port_num:
        try:
            target_ip = socket.gethostbyname(target)
        except OSError:
            print("[^] Cannot resolve {}".format(target))
            return

        try:
            target_name = socket.gethostbyaddr(target_ip)
            print("[*] Scan results for {}".format(target_name[0]))
        except OSError:
            print("[*] Scan results for {}".format(target_ip))

        t = threading.Thread(target=connection_scan, args=(target, int(x)))
        t.start()


def argument_parser():
    parser = argparse.ArgumentParser(description="TCP port scanner")
    parser.add_argument("-o", "--host", nargs="?", help="Host IP Address")
    parser.add_argument("-p", "--ports", nargs="?", help="Comma-separated port list")


def execute():
    module = int(input("Enter the program to run: "))
    options = [1, 2, 3]

    def running():
        if module == 1:
            password_cracker()
        elif module == 2:
            connection_scan()
        elif module == 3:
            port_scan()

    while module not in options:
        module = int(input("Enter a feasible option: "))
    else:
        running()


if __name__ == "__main__":
    execute()
