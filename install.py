import os
import subprocess
import json

DIR_LOGIN = 'login'
FILE_LOGIN = 'login.json'
DIR_TMP = 'tmp'
FILE_TMP_FOLLOWER = 'tmp_follower.txt'
FILE_TMP_FOLLOWING = 'tmp_following.txt'

def install_from_requirements():
    subprocess.run("python -m pip install -r requirements.txt")

def create_directories():
    # If the the login folder does not yet exist, make it exist.
    if not os.path.exists(DIR_LOGIN):
        os.mkdir(DIR_LOGIN)
    # If the the tmp folder does not yet exist, make it exist.
    if not os.path.exists(DIR_TMP):
        os.mkdir(DIR_TMP)

def create_files():
    f = open(DIR_TMP + getFilepathDelimiter() + FILE_TMP_FOLLOWER, 'w+')
    f.close()
    f = open(DIR_TMP + getFilepathDelimiter() + FILE_TMP_FOLLOWING, 'w+')
    f.close()

    # If the file does not yet exist, make it and allow the user to input information
    if os.path.exists(DIR_LOGIN + getFilepathDelimiter() + FILE_LOGIN):

        print("Login information detected. Would you like to re-enter it? [Y/N]: ")

        option = input()
        if str(option).lower() == 'n':
            return
    
    f = open(DIR_LOGIN + getFilepathDelimiter() + FILE_LOGIN, 'w+')
    
    email = input("Email: ")
    username = input("Username: ")
    password = input("Password: ")
    f.write('{\n\t"email": "' + str(email) + '",'
            + '\n\t"username": "' + str(username) + '",'
            +'\n\t"password": "' + str(password) + '"\n}')

    f.close()

def getFilepathDelimiter():
    if os.name == 'nt':
        return "\\"
    else:
        return "/"

def main():
    create_directories()
    create_files()
    install_from_requirements()

if __name__ == "__main__":
    main()
