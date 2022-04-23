import argparse
import os
import sys
import time
import glob
import string
import random
import hasher
import shutil

PASSWORD_LEN      = 2
TABLE_FILE        = 'user_table.txt'
UNSALTED_FILE     = 'shadow_no_salt.txt'
SALTED_FILE       = 'shadow_salt.txt'
ENECRYPTED_HEADER = 'encrypted/'
LEGAL_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
NAMES = [
    'James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph',
    'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy',
    'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
    'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna',
    'Joshua', 'Michelle', 'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda',
    'George', 'Melissa', 'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy',
    'Rebecca', 'Jason', 'Sharon', 'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob',
    'Kathleen', 'Gary', 'Amy', 'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan',
    'Helen', 'Stephen', 'Anna', 'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole',
    'Brandon', 'Emma', 'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Gregory',
    'Christine', 'Frank', 'Debra', 'Alexander', 'Rachel', 'Raymond', 'Catherine',
    'Patrick', 'Carolyn', 'Jack', 'Janet', 'Dennis', 'Ruth', 'Jerry', 'Maria',
    'Tyler', 'Heather', 'Aaron', 'Diane', 'Jose', 'Virginia', 'Adam', 'Julie',
    'Henry', 'Joyce', 'Nathan', 'Victoria', 'Douglas', 'Olivia', 'Zachary', 'Kelly',
    'Peter', 'Christina', 'Kyle', 'Lauren', 'Walter', 'Joan', 'Ethan', 'Evelyn',
    'Jeremy', 'Judith', 'Harold', 'Megan', 'Keith', 'Cheryl', 'Christian', 'Andrea',
    'Roger', 'Hannah', 'Noah', 'Martha', 'Gerald', 'Jacqueline', 'Carl', 'Frances',
    'Terry', 'Gloria', 'Sean', 'Ann', 'Austin', 'Teresa', 'Arthur', 'Kathryn',
    'Lawrence', 'Sara', 'Jesse', 'Janice', 'Dylan', 'Jean', 'Bryan', 'Alice', 'Joe',
    'Madison', 'Jordan', 'Doris', 'Billy', 'Abigail', 'Bruce', 'Julia', 'Albert',
    'Judy', 'Willie', 'Grace', 'Gabriel', 'Denise', 'Logan', 'Amber', 'Alan',
    'Marilyn', 'Juan', 'Beverly', 'Wayne', 'Danielle', 'Roy', 'Theresa', 'Ralph',
    'Sophia', 'Randy', 'Marie', 'Eugene', 'Diana', 'Vincent', 'Brittany', 'Russell',
    'Natalie', 'Elijah', 'Isabella', 'Louis', 'Charlotte', 'Bobby', 'Rose', 'Philip',
    'Alexis', 'Johnny', 'Kayla'
]

parser = argparse.ArgumentParser(description="Table filler")
parser.add_argument('--build', type=int,
                    help='Will build a table of NUM_USERS users')
parser.add_argument('--populate', choices=['salted', 'unsalted', 'encrypted'],
                    help='Populate a table of choice with the users from the table\n')
parser.add_argument('--clean', action="store_true", help="cleanup")
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def main():
    if args.build:
        build(args.build)
    elif args.populate:
        start = time.time()
        if args.populate == 'unsalted':
            populate_unsalted()
        if args.populate == 'salted':
            populate_salted()
        if args.populate == 'encrypted':
            populate_encrypted()
        end = time.time()
        print(
            f'populated {args.populate} table of {numUsers} users in {time_formater(end-start)}')
        with open('reportfile.txt', 'a') as report:
            report.write(f'{type}'.ljust(10)+f'{end-start}\n')
    elif args.clean:
        cleaner()


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
        password = ''.join(random.choice(LEGAL_CHARS)
                           for _ in range(PASSWORD_LEN))
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
            counter += 1
            print(f'read {counter} lines of table', end='\r')
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
        print(f'Added {i+1} of {size} unsalted users \{round((i+1)/size*100,1)}% complete', end='\r')
    print('')
    return size


def populate_salted():
    table = readTable()
    size = len(table)
    for i, usr in enumerate(table):
        username, password = usr
        hasher.log_new_user_salted(username, password)
        print(f'Added {i+1} of {size} salted users {round((i+1)/size*100,1)}% complete', end='\r')
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
        print(f'Added {i+1} of {size} encrypted users {round((i+1)/size*100,1)}% complete', end='\r')
    print('')
    return size


def cleaner():
    open('reportfile.txt', 'w').close()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    counter = 0
    numfiles = len(files)
    printed = False
    for f in files:
        if '-gmail' in f:
            os.remove(f)
            counter += 1
            print(f'removed {counter} file of {numfiles} total files', end='\r')
            printed = True
    if printed:
        print('')
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


def getFileNames(username: str) -> str:
    return (
        username.replace('@', '-').replace('.com', '')+'.enc',
        username.replace('@', '-').replace('.com', '')+'.slt'
    )


if __name__ == '__main__':
    main()
