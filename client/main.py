import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import cryptography
import random
from getpass4 import getpass
import base64
from cryptography.fernet import Fernet
import requests
servers = ['localhost:8000']
# derive

def genKey(pw):
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b"salt",
    iterations=1000000,
    backend=default_backend()
  )
  key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
  return key
print("-- WELCOME TO NUCLEUS SECURE DATA TRANSFER --")
option = input('Would you like to check for new information, or send out a FLASH Alert? ')
if option == "1":
  print("-- CHECKING FOR NEW INFORMATION --")
  password = getpass("Enter your password: ")
  key = genKey(password)
  server = random.choice(servers)
  try:
    messages = requests.get("http://"+server+'/receiveMessages').json()
    for message in messages:
      print("--MESSAGE RECEIVED--")
      print("--ATTEMPTING DECRYPT--")
      f = Fernet(key)
      try:
        decrypted = f.decrypt(message.encode()).decode()
        print("--DECRYPTED DATA--")
        print(decrypted)
        del decrypted
      
      except cryptography.fernet.InvalidToken:
        print("--DECRYPTION FAILED--")
      del f
      del key
    else:
      print("--NO NEW INFORMATION--")
  except requests.exceptions.RequestException:
    print("That server is offline. Try again.")
elif option == "2":
  password = getpass("Enter your password: ")
  key = genKey(password)
  server = random.choice(servers)
  msg = getpass("What message are you uplinking? ")
  f = Fernet(key)
  try:
    messages = requests.get("http://"+server+'/uplinkMessage',params={"message":f.encrypt(msg.encode())})
    del f
    print("-- MESSAGE UPLINKED --")
  except requests.exceptions.RequestException:
    print("That server is down, try again later.")
else:
  print("Invalid option")
  exit()