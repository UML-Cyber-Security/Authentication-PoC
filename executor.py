import hasher
import os
import sys
import stdiomask

SALT_FILE = 'shadow_salt.txt'
NO_SALT_FILE = 'shadow_no_salt.txt'

# makes sure file exists
def startfile():
  if not os.path.exists(SALT_FILE):
    with open(SALT_FILE, 'w'):pass


def add_usr():
  username = input('  Username: ')
  password1 = stdiomask.getpass(prompt='     Enter Password: ')
  password2 = stdiomask.getpass(prompt='  Re-enter Password: ')
  if password1 != password2: 
    print('  Passwords did not match')
    return

  content = hasher.register_account(username, password1)
  with open(SALT_FILE, 'a') as fOut:
    fOut.write(f'{content}\n')


def clean_file():
  with open(SALT_FILE, 'w') as fOut:
    fOut.truncate(0)
  with open(NO_SALT_FILE, 'w') as fOut:
    fOut.truncate(0)
  print('  files cleaned')


def kill_file():
  if os.path.exists(SALT_FILE):
    os.remove(SALT_FILE)
  if os.path.exists(NO_SALT_FILE):
    os.remove(NO_SALT_FILE)
    print('  files removed')


def num_format(number):
  if 3 < number < 20: return f'{number}th'
    
  remainder = number % 10
  if remainder == 1: return f'{number}st'
  if remainder == 2: return f'{number}nd'
  if remainder == 3: return f'{number}ed'
  return f'{number}th'


def login():
  username = input('  Username: ')
  password = stdiomask.getpass(prompt='  Password: ')
  with open('shadow.txt', 'r') as fIn:
    lines = fIn.readlines()
  for i, line in enumerate(lines):
    name, salt, hash = linux_line_split(line)
    if name == -1 or name != username: 
      continue
    if eval(hash) == hasher.calc_hash(eval(salt), password):
      safe_password = '*' * len(password)
      print(f'  user {username} with password {safe_password} is the {num_format(i + 1)} user')
      return True
  return False


def linux_line_split(line):
  if ':' not in line or '$' not in line:
    return -1,-1,-1
  return line[:line.index(':')], line[line.index(':') + 1:line.index('$')], line[line.index('$') + 1:]
  

def help():
  print("""Comands:
  'add user'  - adds a new user
  'login'     - lets you try to login
  'make clean'- removes the shadow.txt file
  'length'    - returns the number of users currently reccorded
  'help'      - prints this menu
  'quit''exit'- closes the program""")


def get_num_users():
  with open(SALT_FILE, 'r') as fIn:
    return fIn.read().count('\n')
  

def listen():
  print('Welcome to executor.listen(), we are emulating the linux shadow\nwrite help for more options')
  startfile()
  leave_request = ['q', 'quit', 'exit', 'leave']
  log_request = ['log', 'login', 'log in', 'check usr', 'check user']
  
  dont_quit = True
  while dont_quit:
    comand = input('$ ').lower()

    if comand in leave_request:
      dont_quit = False
      break

    elif comand == 'make clean' or comand == 'clean file':
      kill_file()
      continue
    elif comand == 'clear file':
      clean_file()
      continue

    elif comand == 'add usr' or comand == 'add user':
      add_usr()
      continue

    elif comand in log_request:
      status = login()
      if not status:
        print('  login failed')

    elif comand == 'help':
      help()
      continue

    elif comand == 'length':
      print(f'  There are {get_num_users()} users reccorded in the shadow.txt file at the moment')
      continue


if __name__ == '__main__':
  if len(sys.argv) == 2 and sys.argv[1] == 'help':
    print('The executor.py file was built to let you manually add users and check user-pswd combinations for validity')
    print('python3 executor.py\n\tWill run the manual prompt to add users and log in etc')
    print('python3 executor.py help\n\tWill display the message above')
  else:
    listen()