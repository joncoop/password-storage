import hashlib
import random
import time
#import getpass


# Settings
DATA_FILE = 'users.txt'
USE_SALT = True
SALT_LENGTH = 32
UNSUCCESSFUL_LOGIN_DELAY = 2


def menu():
    while True:
        print("1. Create account")
        print("2. Login")
        print("3. Quit")
        choice = input("> ")

        if choice in ['1', '2', '3']:
            return choice

def get_user_info(user_name):
    with open(DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            user_info = line.split(',')

            name = user_info[0]
            
            if user_name == name:
                return user_info
            
    return None
      
def login():
    user_name = input('Username: ')
    password = input('Password: ')
    #password = getpass.getpass('Password: ')

    user_info = get_user_info(user_name)

    if user_info is not None:
        salt = user_info[1]
        hashed_pw = user_info[2]

        if generate_hash(password + salt) == hashed_pw:
            return True, user_info
    else:
        return False, None
                
def generate_salt():
    hex_chars = '0123456789abcdef'

    salt = ''
    for i in range(SALT_LENGTH):
        salt += random.choice(hex_chars)        

    return salt

def generate_hash(string):
    result = hashlib.sha256(string.encode())
    return result.hexdigest()

def create_account():
    user_name = input('Username: ')
    password = input('Password: ')

    salt = ''
    if USE_SALT:
        salt = generate_salt()
        password += salt
        
    hashed_pass = generate_hash(password)
    
    with open('users.txt', 'a') as f:
        f.write(user_name + ',' + salt + ',' + hashed_pass + '\n')

def do_secret_stuff(user_info):
    name = user_info[0]
    print('You can type anything here, ' + name + ' When your done, type \'logout\'.')
    logged_in = True

    while logged_in:
        command = input('> ')
        if command == 'logout':
            logged_in = False
            
def run():
    running = True
    
    while running:
        choice = menu()

        if choice == '1':
            create_account()
        elif choice == '2':
            success, user_info = login()

            if success:
                print('Access Granted!')
                do_secret_stuff(user_info)
            else:
                time.sleep(UNSUCCESSFUL_LOGIN_DELAY)
                print('Access Denied!')
        
        elif choice == '3':
            running = False
    
if __name__ == "__main__":
    run()
