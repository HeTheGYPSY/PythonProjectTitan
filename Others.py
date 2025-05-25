import re
import subprocess


def installations():
    packages = ["google-auth-oauth", "milk", "tensorflow"]
    for package in packages:
        subprocess.run(f"pip3 install {package}")
    else:
        print("Installation Completed!")


def listing():
    listing = subprocess.run("pip list", capture_output=True).stdout.decode()
    for i in range(0, 10):
        for j in range(0, 10):
            for k in range(0, 10):
                arguments = set(re.findall(f"(.*)=={i}.{j}.{k}", listing))
    edited = []
    for item in arguments:
        if item != '':
            edited.append(item)
    print(edited)


def lister():
    listing = subprocess.run("pip list", capture_output=True).stdout.decode()
    arguments = set(re.findall(f"(.*)\s\s", listing))
    edited = []
    for item in arguments:
        if item != '':
            edited.append(item.rstrip("\s(.*)"))
    print(edited)


if __name__=='__main__':
    lister()
