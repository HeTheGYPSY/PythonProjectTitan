import subprocess


def installations():
    packages = ["google-auth-oauth", "milk", "tensorflow"]
    for package in packages:
        subprocess.run(f"pip3 install {package}")
    else:
        print("Installation Completed!")


if __name__=='__main__':
    installations()
