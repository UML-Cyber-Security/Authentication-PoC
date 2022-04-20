import os
import sys
import time
import glob
import string
import random
import hasher
import shutil

PASSWORD_LEN = 2
TABLE_FILE        = 'user_table.txt'
UNSALTED_FILE     = 'shadow_no_salt.txt'
SALTED_FILE       = 'shadow_salt.txt'
ENECRYPTED_HEADER = 'encrypted/'
LEGAL_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
NAMES = [
  'James','Mary','Robert','Patricia','John','Jennifer','Michael','Linda',
  'William','Elizabeth','David','Barbara','Richard','Susan','Joseph',
  'Jessica','Thomas','Sarah','Charles','Karen','Christopher','Nancy',
  'Daniel','Lisa','Matthew','Betty','Anthony','Margaret','Mark','Sandra',
  'Donald','Ashley','Steven','Kimberly','Paul','Emily','Andrew','Donna',
  'Joshua','Michelle','Kenneth','Dorothy','Kevin','Carol','Brian','Amanda',
  'George','Melissa','Edward','Deborah','Ronald','Stephanie','Timothy',
  'Rebecca','Jason','Sharon','Jeffrey','Laura','Ryan','Cynthia','Jacob',
  'Kathleen','Gary','Amy','Nicholas','Shirley','Eric','Angela','Jonathan', 
  'Helen','Stephen','Anna','Larry','Brenda','Justin','Pamela','Scott','Nicole',
  'Brandon','Emma','Benjamin','Samantha','Samuel','Katherine','Gregory',
  'Christine','Frank','Debra','Alexander','Rachel','Raymond','Catherine',
  'Patrick','Carolyn','Jack','Janet','Dennis','Ruth','Jerry','Maria',
  'Tyler','Heather','Aaron','Diane','Jose','Virginia','Adam','Julie',
  'Henry','Joyce','Nathan','Victoria','Douglas','Olivia','Zachary','Kelly',
  'Peter','Christina','Kyle','Lauren','Walter','Joan','Ethan','Evelyn',
  'Jeremy','Judith','Harold','Megan','Keith','Cheryl','Christian','Andrea',
  'Roger','Hannah','Noah','Martha','Gerald','Jacqueline','Carl','Frances',
  'Terry','Gloria','Sean','Ann','Austin','Teresa','Arthur','Kathryn',
  'Lawrence','Sara','Jesse','Janice','Dylan','Jean','Bryan','Alice','Joe',
  'Madison','Jordan','Doris','Billy','Abigail','Bruce','Julia','Albert',
  'Judy','Willie','Grace','Gabriel','Denise','Logan','Amber','Alan',
  'Marilyn','Juan','Beverly','Wayne','Danielle','Roy','Theresa','Ralph',
  'Sophia','Randy','Marie','Eugene','Diana','Vincent','Brittany','Russell',
  'Natalie','Elijah','Isabella','Louis','Charlotte','Bobby','Rose','Philip',
  'Alexis','Johnny','Kayla'
]

def main():
  if len(sys.argv) == 1:
    print('run python3 filler.py help - for more options')
    return
  if len(sys.argv) == 2:
    if sys.argv[1] == 'help':
      print('Filler.py:\n$ python3 filler.py build <NUM_USERS>\n\tWill build a table of NUM_USERS users')
      print('$ python3 filler.py populate unsalted\n\tWill populate an unsalted table with the users from the table\n\tTime this operation with "-t" command at the end of the call')
      print('$ python3 filler.py populate salted\n\tWill populate a salted table with the users from the table\n\tTime this operation with "-t" command at the end of the call')
      print('$ python3 filler.py help\n\tWill show this message\n')
      return
  elif len(sys.argv) == 3:
    if sys.argv[1] == 'build':
      try:
        numIter = int(sys.argv[2])
      except:
        numIter = True
        while numIter:
          try:
            numIter = int(input("sorry, couldn't understand the last input, how many would you like to build? "))
          except:
            numIter = True
      build(numIter)
      return
    elif sys.argv[1] == 'populate':
      if sys.argv[2] == 'unsalted':
        populate_unsalted()
        return
      if sys.argv[2] == 'salted':
        populate_salted()
        return
      if sys.argv[2] == 'encrypted':
        populate_encrypted()
        return
    elif sys.argv[1] == 'make' and sys.argv[2] == 'clean':
      cleaner()
      return
    else:
      print(f'"{sys.argv[1]}" is an unknwon command, try "python3 filler.py help" for more options')
      return
  elif len(sys.argv) == 4:
    legal_salt_type = ['unsalted', 'salted', 'encrypted']
    if sys.argv[1] == 'populate' and sys.argv[2] in legal_salt_type and sys.argv[3] == '-t':
      type = 'encrypted'
      if sys.argv[2] == 'unsalted':
        type = 'unsalted'
        start = time.time()
        numUsers = populate_unsalted()
        end = time.time()
      elif sys.argv[2] == 'salted':
        type = 'salted'
        start = time.time()
        numUsers = populate_salted()
        end = time.time()
      else:
        start = time.time()
        numUsers = populate_encrypted()
        end = time.time()
      print(f'populated {type} table of {numUsers} users in {time_formater(end-start)}')
      with open('reportfile.txt', 'a') as report:
        report.write(f'{type}'.ljust(10)+f'{end-start}\n')
      return
  print(f'{sys.argv[1]} is an unknwon command, try "python3 filler.py help" for more options')
  return
      

def time_formater(time_in_seconds):
  if time_in_seconds < 1:
    return f'{time_in_seconds * 1000} milliseconds'
  if time_in_seconds < 60:
    return f'{int(time_in_seconds)} seconds and {time_in_seconds * 1000 % 1000} milliseconds'
  if time_in_seconds < 3600:
    return f'{time_in_seconds // 60} minutes and {time_in_seconds % 60} seconds'
  return f'{time_in_seconds // 3600} hours, {time_in_seconds // 60} minutes, and {time_in_seconds % 60} seconds'


def build(numIter):
  for i in range(numIter):
    username = f'{NAMES[i]}@gmail.com'
    password = ''.join(random.choice(LEGAL_CHARS) for _ in range(PASSWORD_LEN))
    with open(TABLE_FILE, 'a') as table:
      table.write(f'usr={username}'.ljust(27)+f'pwd={password}\n')
  print(f'User table built successfully with {numIter} users')


def readTable():
  out_list = []
  with open(TABLE_FILE, 'r') as table:
    line = 'blank'
    counter = 0
    while not not line:
      line = table.readline()
      if 'usr=' not in line or 'pwd=' not in line:
        continue
      counter+=1
      print(f'read {counter} lines of table',end='\r')
      out_list.append(
        (
          line[4:line.index(' ')],
          line[31:-1]
        )
      )
    print('')
  return out_list


def populate_unsalted():
  table = readTable()
  size = len(table)
  for i, usr in enumerate(table):
    username, password = usr
    hasher.log_new_user_unsalted(username, password)
    print(f'Added {i+1} of {size} unsalted users {round((i+1)/size*100,1)}% complete',end='\r')
  print('')
  return size


def populate_salted():
  table = readTable()
  size = len(table)
  for i, usr in enumerate(table):
    username, password = usr
    hasher.log_new_user_salted(username, password)
    print(f'Added {i+1} of {size} salted users {round((i+1)/size*100,1)}% complete',end='\r')
  print('')
  return size


def populate_encrypted():
  table = readTable()
  size = len(table)
  path = ENECRYPTED_HEADER
  if not os.path.exists(path):
    os.makedirs(path)
  for i, usr in enumerate(table):
    username, password = usr
    salt, hash = hasher.make_hash(password)
    userFile, saltFile = getFileNames(username)
    with open(os.path.join(path, saltFile), 'wb') as saltfile:
      saltfile.write(salt)
    encBytes = hasher.encrypt_bytes(username, hash)
    with open(os.path.join(path, userFile), 'wb') as encFile:
      encFile.write(encBytes)
    print(f'Added {i+1} of {size} encrypted users {round((i+1)/size*100,1)}% complete',end='\r')
  print('')
  return size


def cleaner():
  open('reportfile.txt', 'w').close()
  files = [f for f in os.listdir('.') if   os.path.isfile(f)]
  counter = 0
  numfiles = len(files)
  printed = False
  for f in files:
    if '-gmail' in f:
      os.remove(f)
      counter+=1
      print(f'removed {counter} file of {numfiles} total files', end='\r')
      printed = True
  if printed: print('')
  print('removed miscellaneous files')
  try:
    shutil.rmtree('encrypted')
    print('encrypted folder removed')
  except:
    print('encrypted folder up to date')
  list_of_files = ['shadow_no_salt.txt', 'shadow_salt.txt', 'user_table.txt']
  for file in list_of_files:
    try:
      os.remove(file)
      print(f'{file} removed')
    except:
      print(f'{file} up to date')


def getFileNames(username:str)->str:
  return (
    username.replace('@', '-').replace('.com','')+'.enc',
    username.replace('@', '-').replace('.com','')+'.slt'
  )


if __name__ == '__main__':
  main()