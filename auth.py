import hashlib
import uuid

salt = ''

def generateHash(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password

def getSalt():
    return salt

def checkPasswd(password, salty, hashed_passwd):
    if hashed_passwd == hashlib.sha512(password + salty).hexdigest(): # If hashed password matches the hash of the password entered then return TRUE; else FALSE 
        return True  
    else:
        return False
