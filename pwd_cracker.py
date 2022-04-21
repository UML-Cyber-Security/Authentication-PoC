import string
import os
import sys
import time
import hasher
from datetime import datetime
LEGAL_LETTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits

def main():
    is_salted = False
    if len(sys.argv) == 1:
        print('for help run "python3 pwd_cracker.py help"')
        responce = 'garbage'
        while responce not in ['n', 'no', 'exit', 'quit', 'q', 'y', 'yes', 'sure', 'ok']:
            responce = input("would you like to continue with default setup? (y/n) ")
            if responce.lower() in ['n', 'no', 'exit', 'quit', 'q']:
                return
        
        start = time.time()
        status = password_cracker('shadow_no_salt.txt', False, ['rb2_unsalted.txt'], 'pawned.txt')
        end = time.time()

    if len(sys.argv) == 2 and sys.argv[1] == 'help':
        print('python3    pwd_cracker.py    <LEAKED_HASH_FILE:str>    <IS_SALTED:bool>    <FILE_NAME_OF_TEXT_FILE_CONTAINING_RAINBOW_TABLE_FILE_NAMES:str>    <OUTPUT_FILE:str>')
        print('python3    pwd_cracker.py    <LEAKED_HASH-FL_DIRECTORY:str> <FILE_CONTAINING_RB-TBL-FL_NAMES:str> <OUTPUT_FILE:str>')
        print('python3    pwd_cracker.py    <LEAKED_HASH-FL_DIRECTORY:str> <FILE_CONTAINING_RB-TBL-FL_NAMES:str> <OUTPUT_FILE:str> -v2\n\tfor faster cracking')
        return
    
    if len(sys.argv) != 5 and len(sys.argv) != 4:
        print(f'Expected 3 or 4 args, recieved {len(sys.argv) - 1} args')
        return
    if len(sys.argv) == 4:
        start = time.time()
        solutions, status = crack_encrypted(groupEncryptedFiles(sys.argv[1]), rainbow_table_agrigator(sys.argv[2]))
        write_solution(solutions, sys.argv[3])
        end = time.time()
        print(f'Time Elapsed: {time_formater(end - start)}                                            ')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with open('timer.txt', 'a') as timer_file:
            timer_file.write(f'Hash-Crack took {time_formater(end - start)}'.ljust(48)+f' at {current_time} (type=encrypted, status={status_formater(status)})\n')
        return

    if sys.argv[4] == '-v2':
        start = time.time()
        solutions, status = crack_encrypted_v2(sys.argv[1], rainbow_table_agrigator(sys.argv[2]))
        write_solution(solutions, sys.argv[3])
        end = time.time()
        print(f'Time Elapsed: {time_formater(end - start)}                                            ')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with open('timer.txt', 'a') as timer_file:
            timer_file.write(f'Hash-Crack took {time_formater(end - start)}'.ljust(48)+f' at {current_time} (type=encrypted, status={status_formater(status)})\n')
        return
    
    start = time.time()
    status = password_cracker(sys.argv[1], bool_maker(sys.argv[2]), rainbow_table_agrigator(sys.argv[3]), sys.argv[4])
    end = time.time()
    print(f'Time Elapsed: {time_formater(end - start)}                                            ')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open('timer.txt', 'a') as timer_file:
        timer_file.write(f'Hash-Crack took {time_formater(end - start)}'.ljust(48)+f' at {current_time} (type={salt_type(is_salted)}, status={status_formater(status)})\n')


def time_formater(time_in_seconds):
    if time_in_seconds < 1:
        return f'{time_in_seconds * 1000} milliseconds'
    if time_in_seconds < 60:
        return f'{int(time_in_seconds)} seconds and {time_in_seconds * 1000 % 1000} milliseconds'
    if time_in_seconds < 3600:
        return f'{time_in_seconds // 60} minutes and {time_in_seconds % 60} seconds'
    return f'{time_in_seconds // 3600} hours, {time_in_seconds // 60} minutes, and {time_in_seconds % 60} seconds'


def bool_maker(sbool:str)->bool:
    if sbool.lower() == 'true': 
        return True
    return False


def rainbow_table_agrigator(file_name)->list:
    with open(file_name, 'r') as file:
        return [line[:-1] for line in file.readlines() if not not line]


def salt_type(is_salted:bool)->str:
    if is_salted: 
        return 'salted'
    return 'unsalted'


def status_formater(status:bool)->str:
    if status:
        return 'complete'
    return 'incomplete'


def password_cracker(shadow_file:str, is_salted:bool, rainbowtables:list, output_file:str) -> bool:
    force(type(shadow_file) == str and type(is_salted) == bool and type(rainbowtables) == list and type(output_file) == str)
    if not is_salted:
        return crack_unsalted(shadow_file, rainbowtables[0], output_file)
    return crack_salted(shadow_file, rainbowtables, output_file)


def crack_salted(shadow_file:str, rainbowtables:list, output_file:str) -> bool:
    with open(shadow_file, 'r') as fIn:
        shadow_vars = [
            (
                line[ : line.index(':') ],
                line[ line.index(':')+1 : line.index('$') ],
                line[ line.index('$')+1 : -1 ]
            )
            for line in fIn.readlines()
            if ':' in line and '$' in line
        ]
    registrar = tupler(shadow_vars)
    size = len(shadow_vars)
    counter = 0
    print(f'cracked {counter} of {size} aprox {round(counter / size * 100,2)}% complete', end='\r')

    for i in range(len(registrar)):
        if registrar[i] == None:
            continue
        with open(rainbowtables[i], 'r') as rainbowTable:
            cur_registry = registrar[i]
            for line_number, line in enumerate(rainbowTable.readlines()):
                for r_index, (name, salt, hash) in enumerate(cur_registry):
                    if line[:-1] == hash:
                        del cur_registry[r_index]
                        with open(output_file, 'a') as out:
                            out.write(f'{name}:{compute_password(line_number)}\n')
                        counter += 1
                        print(f'cracked {counter} of {size} aprox {round(counter / size * 100,2)}% complete', end='\r')
            if len(cur_registry) == 1:
                break
            
            
                        
                        
                        



'''
    for username, salt, hash in shadow_vars:
        with open(rainbowtables[salt_decoder(salt)], 'r') as rainbow_table:
            rainbow_hash = rainbow_table.readline()
            rcounter = 0
            cracked = False
            while rainbow_hash:
                # make sure it's not an eof python-mispointer
                if not rainbow_hash:
                    break
                
                rcounter += 1
                if hash == rainbow_hash:
                    with open(output_file, 'a') as output:
                        output.write(f'{username}:{compute_password(rcounter - 1)}')
                    cracked = True
                    break
            if cracked:
                counter += 1
                print(f'cracked {counter} of {size} aprox {round(counter / size * 100,2)}% complete', end='\r')
            else: 
                fails += 1
                print(f"FAILED TO CRACK {username}'s password, {fails} of size possible {round(fails / size * 100,2)}%")
    if fails == 1:
        print(f'{fails} password crack failed!')
        return False
    print(f'{fails} password cracks failed!')
    if fails == 0:
        return True
    return False'''


# will have 256 members, where each memebr is the list of users
# using that salt
def tupler(regestry:list): 
    salts = [str(bytes([x])) for x in range(256)]
    builder = []
    added = 0
    for salt in salts:
        adder = []
        for user_name, user_salt, user_hash in regestry:
            if user_salt == salt:
                adder.append((user_name, user_salt, user_hash))
                added += 1
        if len(adder) != 0:
            builder.append(adder)
        else:
            builder.append(None)
    if len(builder) != 256: 
        print(f'Missing elements, expected 256, got {len(builder)}')
        print(builder)
    return builder
    

def salt_decoder(salt):
    return int.from_bytes(salt, "big")
    

def crack_unsalted(shadow_file:str, rainbowtable:str, output_file:str) -> bool:
    with open(shadow_file, 'r') as fIn:
        content = fIn.readlines()
    shadow_hashes = [line[line.index(':')+1:-1] for line in content if ':' in line]
    shadow_users = [line[:line.index(':')] for line in content if ':' in line]
    size = len(shadow_hashes)
    counter = 0
    print(f'cracked {counter} of {size}, {round(counter / size * 100,2)}% complete', end='\r')
    
    with open(rainbowtable, 'r') as rainbow_table:
        rcounter = 0
        hcounter = 0
        hash = rainbow_table.readline()[:-1]
        while hash:
            hcounter += 1
            if not hash:
                break
                
            rcounter += 1
            while hash in shadow_hashes:
                with open(output_file, 'a') as output:
                    indx_found = shadow_hashes.index(hash)
                    output.write(f'{shadow_users[indx_found]}:{compute_password(rcounter - 1)}\n')
                counter += 1
                print(f'cracked {counter} of {size} aprox {round(counter / size * 100,2)}% complete', end='\r')
                if counter == len(shadow_hashes): # end early if all are found
                    break
                del shadow_hashes[indx_found]
                del shadow_users[indx_found]
            hash = rainbow_table.readline()[:-1]

    print('')
    if size - counter == 1:
        print(f'{size - counter} password crack failed!')
        print(f'searched through {hcounter} hashes')
        return False
    print(f'{size - counter} password cracks failed!')
    print(f'searched through {hcounter} hashes')
    if size - counter == 0:
        return True
    return False
    

def compute_password(line_number):
    return f'{LEGAL_LETTERS[line_number // 62]}{LEGAL_LETTERS[line_number % 62]}'
                

def force(condition:bool):
    if type(condition) != bool or not condition:
        print('conditions failed')
        quit()

def crack_encrypted(file_tuples:list, rainbow_tables:list):
    size = len(file_tuples)
    failed = 0
    solutions = []
    print(f'cracked 0, failed 0 of {size} aprox 0% complete', end='\r')
    for i, (username, sltFile, encFile) in enumerate(file_tuples):
        index = getSaltIndex(sltFile)
        if index == -1:
            print(f'\n{index=}')
            failed += 1
            print(f'cracked {i - failed + 1}, failed {failed} of {size} aprox {round((i+1)/size*100,1)}% complete', end='\r')
            continue
        with open(encFile, 'rb') as binEncFile:
            usrbytes = binEncFile.read()
        with open(rainbow_tables[index], 'r') as rainbowTable:
            rbLines = [line[:-1] for line in rainbowTable.readlines()]
        cracked = False
        for iHash, hash in enumerate(rbLines):
            hash = (hash[2:-1]).encode().decode('unicode_escape').encode("raw_unicode_escape")
            try:
                plain_text = hasher.decrypt_bytes(usrbytes, hash)
                #username.encode(), 
                flagged = False
            except:
                plain_text = -1
                flagged = True
                
            if not flagged and plain_text == username:
                solutions.append((username,compute_password(iHash)))
                print(f'cracked {i - failed + 1}, failed {failed} of {size} aprox {round((i+1)/size*100,1)}% complete', end='\r')
                cracked = True
                break
            
        if not cracked:
            failed +=1
            print(f'cracked {i - failed + 1}, failed {failed} of {size} aprox {round((i+1)/size*100,1)}% complete', end='\r')
    print('')
    return solutions, (failed == 0)
            
        
def write_solution(solutions, output_file):
    for username, password in solutions:
        with open(output_file, 'a') as output:
            output.write(f'{username}:{password}\n')
            

def getSaltIndex(slt_file):
    possible_salts = [bytes([x]) for x in range(256)]
    with open(slt_file, 'rb') as sfile:
        slt = sfile.read()
    for i, pSalt in enumerate(possible_salts):
        if slt == pSalt:
            return i
    return -1


def crack_encrypted_v2(dir:str, rainbow_tables:list):
    encContentLst = getEncryptedFileContent(dir)
    size = len(encContentLst)
    counter = 0
    failed = 0
    solutions = []
    print(f'cracked 0, failed 0 of {size} aprox 0% complete', end='\r')
    for index, pack in enumerate(encContentLst):
        if pack == None:
            continue
        try:
            usernames, encBytes = pack # unpack lol
        except:
            print(pack)
            return
        with open(rainbow_tables[index], 'r') as rb_table:
            rb_lines = [line[2:-2] for line in rb_table.readlines()]
        users_per_salt = len(usernames)
        counter += users_per_salt
        for i, line in enumerate(rb_lines):
            hash = line.encode().decode('unicode_escape').encode("raw_unicode_escape")
            for user_index, usrbytes in enumerate(encBytes):
                username = usernames[user_index]
                try:
                    plain_text = hasher.decrypt_bytes(usrbytes, hash)
                except:
                    plain_text = -1
            if plain_text != -1 and plain_text == username:
                solutions.append((
                    username,
                    compute_password(user_index)
                ))
                print(f'cracked {counter - failed + 1}, failed {failed} of {size} aprox {round((counter+1)/size*100,1)}% complete', end='\r')
                users_per_salt -= 1
        if users_per_salt > 0:
            failed += users_per_salt
            print(f'cracked {counter - failed + 1}, failed {failed} of {size} aprox {round((counter+1)/size*100,1)}% complete', end='\r')
    print('')
    return solutions, (failed == 0)


def getEncryptedFileContent(dir):
    lstBuilder = [ [], [], [] ] # three list tuple
    for name, sltFl, encFl in groupEncryptedFiles(dir):
        with open(sltFl, 'rb') as f_in:
            sltBytes = f_in.read()
        with open(encFl, 'rb') as f_in:
            encBytes = f_in.read()
        lstBuilder[0] += [name]
        lstBuilder[1] += [sltBytes]
        lstBuilder[2] += [encBytes]
    return orderEncLst( # returns one list of tuples
        lstBuilder[0],        # for "efficiency"
        lstBuilder[1], 
        lstBuilder[2]
    )


def orderEncLst(names, slts, encs):
    list_of_salts = [bytes([x]) for x in range(256)]
    orgLst = []
    for salt in list_of_salts:
        if salt not in slts:
            orgLst.append(None)
            continue
            
        buff = [[],[]]
        while salt in slts:
            index = slts.index(salt)
            buff[0].append(names[index])
            buff[1].append(encs[index])
            #     names[index], # do not add the salt, it's assumed
            #     encs[index]
            # ))
            del names[index]
            del slts[index]
            del encs[index]
        orgLst.append(buff)
        if len(slts) == 0:
            break # cut short if end for optimisation
    return orgLst


def groupEncryptedFiles(dir):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        files.extend(filenames)
    return [
        (
            nameConverter(filename[:-4]), 
            f'{dir}/{filename[:-3]}slt', 
            f'{dir}/{filename}'
        ) 
        for filename in files 
        if filename[-4:] == '.enc'
    ]


def nameConverter(filename):
    return filename.replace('-','@') + '.com'


if __name__ == '__main__':
    main()