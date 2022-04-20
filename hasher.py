from hashlib import pbkdf2_hmac as hash_algo
from os import urandom
import sys
import base64
from cryptography.fernet import Fernet
SALT_FILE = 'shadow_salt.txt'
NO_SALT_FILE = 'shadow_no_salt.txt'

def make_hash(password):
  salt = urandom(1)
  key = hash_algo('sha256', password.encode('utf-8'), salt, 100000)
  return salt, key

def calc_hash(salt, password):
  return hash_algo('sha256', password.encode('utf-8'), salt, 100000)

def register_account(usr_name, usr_pass):
  salt, hash = make_hash(usr_pass)
  return f'{usr_name}:{salt}${hash}'

def log_new_user_salted(username, user_password):
  salt, hash = make_hash(user_password)
  with open(SALT_FILE, 'a') as fOut:
    fOut.write(f'{username}:{salt}${hash}\n')

  
def log_new_user_unsalted(username, user_password):
  hash = make_unsalted_hash(user_password)
  with open(NO_SALT_FILE, 'a') as fOut:
    fOut.write(f'{username}:{hash}\n')


def make_unsalted_hash(password):
  return hash_algo('sha256', password.encode('utf-8'), bytes(), 100000)


def encrypt_bytes(nons, hash) -> bytes:
  fer = Fernet(
    base64.urlsafe_b64encode(
      hash
    )
  )
  return fer.encrypt(
    base64.urlsafe_b64encode(
      nons.encode()
    )
  )

if __name__ == '__main__':
  if len(sys.argv) == 2 and sys.argv[1] == 'help':
    print('Hasher.py\nThis python file is made to hash and encrypt passwords and user data')
    print('This python file is not made not be run by the user, but instead to be used as a helper file')


def encrypt_bytes_from(orgBytes, encryption_key):
  key = base64.urlsafe_b64encode(encryption_key)
  fer = Fernet(key)
  return fer.encrypt(orgBytes)


def decrypt_bytes(orgBytes, encryption_key):
  fer = Fernet(
    base64.urlsafe_b64encode(
      encryption_key
    )
  )
  return base64.urlsafe_b64decode(
    fer.decrypt(
      orgBytes
    )
  ).decode()