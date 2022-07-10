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
import time
servers = ['localhost:8000']#['34.238.44.100:8000','44.203.116.175:8000']
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
name = input("ENTER YOUR IDENTIFIER: ")
while True:
  option = input('Would you like to check for new information, send out a FLASH Alert, or do a server status check? ')
  if option == "1":
    print("-- CHECKING FOR NEW INFORMATION --")
    password = getpass("Enter your password: ")
    key = genKey(password)
    server = random.choice(servers)
    print(server)
    try:
      messages = requests.get("http://"+server+'/receiveMessages').json()
      for message in messages:
        print("--MESSAGE RECEIVED--")
        print("--ATTEMPTING DECRYPT--")
        f = Fernet(key)
        try:
          decrypted = f.decrypt(message['content'].encode()).decode()
          sender = f.decrypt(message['sender'].encode()).decode()
          print("--DECRYPTED DATA--")
          print(sender+": "+decrypted)
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
      for server in servers:
        messages = requests.get("http://"+server+'/uplinkMessage',params={"message":f.encrypt(msg.encode()),"sender":f.encrypt(name.encode())}).json()
      del f
      print("-- MESSAGE UPLINKED --")
    except requests.exceptions.RequestException:
      print("That server is down, try again later.")

  elif option == "3":
    for server in servers:
      try:
        lbf = time.time()
        requests.get("http://"+server+'/onlineCheck')
        lba = time.time()
        print("Server "+server+" is online. Latency: "+str(round((lba-lbf)*1000,1))+"ms")
      except requests.exceptions.RequestException as e:
        print("Server "+server+" is offline.",str(e))
  
  elif option == "4":
    print("--BACKEND MODE--")
    backend = input("Would you like to commense a File Integrity Test? ")
    if backend == "1":
      print("--FILE INTEGRITY TEST--")
      checksums = []
      for server in servers:
        try:
          integTest = requests.get('http://'+server+'/integrityTest')
        except requests.exceptions.RequestException:
          print("Server "+server+" is offline.")
        checksums.append(integTest.json())
        cs = []
        [cs.append(x) for x in checksums if x not in cs]
        if len(cs) == 1:
          print("--INTEGRITY TEST PASSED--")
        else:
          print("--INTEGRITY TEST FAILED--")
  else:
    print("Invalid option")
    exit()
