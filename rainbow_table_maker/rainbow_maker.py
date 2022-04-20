import string
from hashlib import pbkdf2_hmac as hash_algo
import sys
import os

C_FILE = 'counter.txt'


def calc_hash(user_salt, user_password):
    return hash_algo('sha256', user_password.encode('utf-8'), user_salt, 100000)


def num_format(number):
    if 3 < number < 20:
        return f'{number}th'

    remainder = number % 10
    if remainder == 1:
        return f'{number}st'
    if remainder == 2:
        return f'{number}nd'
    if remainder == 3:
        return f'{number}ed'
    return f'{number}th'


def build_rainbow_table(unsalted=False):
    if unsalted:
        if os.path.exists('rb2_unsalted.txt'):
            acc = ['y', 'yes', 'yep', 'yeah', 'sure']
            dec = ['n', 'no', 'quit', 'q', 'exit', 'leave', 'cancel']
            inp = 'garbage'
            while inp not in (acc + dec):
                inp = input('WARNING: The unsalted rainbow table file already exists, would you like to recompute it? (y/n) ')
            if inp in dec:
                print('exiting program...')
                return
        possible_salts = [bytes()]
        num_iter = 3844
    else:
        files_found = 0
        for i in range(256):
            if os.path.exists(f'rb2_{i}.txt'):
                files_found += 1
        if files_found > 0:
            acc = ['y', 'yes', 'yep', 'yeah', 'sure']
            dec = ['n', 'no', 'quit', 'q', 'exit', 'leave', 'cancel']
            inp = 'garbage'
            while inp not in (acc + dec):
                inp = input(
                    f'WARNING: {files_found} salted rainbow table files already exist, would you like to recompute all of them? (y/n) ')
            if inp in dec:
                print('exiting program...')
                return
        possible_salts = [bytes([x]) for x in range(256)]
        num_iter = 984064

    legal_letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    counter = 0
    for i, salt in enumerate(possible_salts):
        iteration = num_format(i + 1)
        with open(C_FILE, 'a') as fOut:
            if unsalted:
                fOut.write(f'started unsalted_file ')
            else:
                fOut.write(f'started {salt} ({iteration} byte) ')
        if unsalted:
            CUR_FILE = 'rb2_unsalted.txt'
        else:
            CUR_FILE = f'rb2_{i}.txt'
        for first_letter in legal_letters:
            with open(CUR_FILE, 'a') as out:
                for second_letter in legal_letters:
                    out.write(
                        f'{calc_hash(salt, first_letter + second_letter)}\n'
                    )  # {first_letter}{second_letter} can be calculated based on line number
                    counter += 1
                    print(
                        f'calculated {counter} of {num_iter}, ' + f'{round(counter / num_iter * 100, 4)}%'.ljust(9) +
                        ' of total : '+f'{round(counter % 3844 / 3844 * 100, 2)}%'.ljust(7) +
                        f' of {iteration} byte   ', end='\r')
        with open(C_FILE, 'a') as fOut:
            fOut.write('✔️\n')
        if unsalted:
            print(f'\nCOMPLETED RAINBOW TABLE!                                                                                  ')
        else:
            print(f'COMPLETED BYTE {salt}! ({iteration} of 256)                                                                                  ')


def count_total_size():
    files = [f'rb2_{x}.txt' for x in range(256)]
    total0, total1 = 0, 0
    for file in files:
        if os.path.exists(file):
            total0 += os.path.getsize(file)
    if os.path.exists('rb2_unsalted.txt'):
        total1 = os.path.getsize('rb2_unsalted.txt')
    return total0, total1


def clean_formal(size_bytes):
    if size_bytes < 1000:
        return f'{size_bytes} bytes'
    if size_bytes < 1000000:
        return f'{round(size_bytes / 1000, 2)} megabytes'
    if size_bytes < 1000000000:
        return f'{round(size_bytes / 1000000, 2)} gigabytes'
    return f'{round(size_bytes / 1000000000, 2)} terabytes'


def main():
    argc = len(sys.argv)
    if argc == 2:
        if sys.argv[1] == 'help':
            print(' > python3 rainbow_maker.py <build>\n\t\tTo build 256 salted rb_tables')
            print(' > python3 rainbow_maker.py <build_unsalted>\n\t\tTo build 1 unsalted rb_table')
            print(' > python3 rainbow_maker.py <size>\n\t\tTo calculate and return the total size used by all rb tables')
        if sys.argv[1] == 'build':
            build_rainbow_table()
            return
        if sys.argv[1] == 'build_unsalted':
            build_rainbow_table(unsalted=True)
            return
        if sys.argv[1] == 'size':
            salted_size, unsalted_size = count_total_size()
            print(f' SIZE: \n   salted  = {clean_formal(salted_size)}\n   unsalted= {clean_formal(unsalted_size)}\n   total   = {clean_formal(salted_size+unsalted_size)}')
            return
    if argc == 1:
        print('  Please run with args: possible args (build, build_unsalted, size)')
        return


if __name__ == '__main__':
    main()
