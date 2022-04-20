import os
import filler
FILE = 'reportfile.txt'
def main():
  rcont = -1
  if os.path.exists(FILE):
    with open(FILE, 'r') as reportfile:
      rcont = reportfile.readlines()
  if rcont == -1:
    print('reportfile.txt missing or empty, time info about shadow file generation lost or missing')
  else:
    time_nosalt, time_salt, time_encr = unpack(rcont)
  space_nosalt, space_salt, space_encr = spaceComplexity()
  print('REPORT:')
  if rcont == -1:
    print('time info could not be found')
  else:
    if time_nosalt == -1:
      print(f'shadow_no_salt.txt could not be found')
    else:
      print(f'shadow_no_salt.txt {filler.time_formater(time_nosalt)}')
    if time_salt == -1:
      print(f'shadow_salt.txt    could not be found')
    else:
      print(f'shadow_salt.txt    {filler.time_formater(time_salt)}')
    if time_encr == -1:
      print(f'encrypted folder   could not be found')
    else:
      print(f'encrypted shadow   {filler.time_formater(time_encr)}')
  if space_nosalt == -1:
    print(f'shadow_no_salt.txt could not be found')
  else:
    print(f'shadow_no_salt.txt {byteFormater(space_nosalt)}')
  if space_salt == -1:
    print(f'shadow_salt.txt    could not be found')
  else:
    print(f'shadow_salt.txt    {byteFormater(space_salt)}')
  if space_encr == 0:
    print(f'encrypted shadow   could not be found')
  else:
    print(f'encrypted shadow   {byteFormater(space_encr)}')
    

def unpack(content):
  noSalt, salt, encr = -1, -1, -1
  for line in content:
    if len(line) < 2 or ' ' not in line:
      continue
    type = line[0:line.index(' ')]
    if type == 'unsalted':
      noSalt = float(line[10:-1])
    elif type == 'salted':
      salt = float(line[10:-1])
    elif type == 'encrypted':
      encr = float(line[10:-1])
  return noSalt, salt, encr


def spaceComplexity():
  noSalt, salt = -1, -1
  if os.path.exists('shadow_no_salt.txt'):
    noSalt = os.path.getsize('shadow_no_salt.txt')
  if os.path.exists('shadow_salt.txt'):
    salt = os.path.getsize('shadow_salt.txt')
  return noSalt, salt, getSizeEncryptedFiles()

  
def getSizeEncryptedFiles():
  f = []
  total = 0
  for (dirpath, dirnames, filenames) in os.walk('encrypted'):
    f.extend(filenames)
  for filename in f:
    path = f'encrypted/{filename}'
    total+=os.path.getsize(path)
  return total


def byteFormater(numbytes):
  if numbytes < 1000:
    return f'{numbytes} b'
  if numbytes < 1000000:
    return f'{round(numbytes/1000, 2)} kb'
  return f'{round(numbytes/1000000, 2)} mb'


if __name__ == '__main__':
  main()
  