#!/usr/bin/python

import json
import jwt
import os 

SECRET_KEY = os.urandom(32)

def authorise(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return False
    
    if "admin" in decoded and decoded["admin"] == "True":
        print("[+] Welcome admin!")
        return True 
    
    if "username" in decoded:
        print(f"[+] Welcome {decoded['username']}")
        return False 
    
    print("[x] Hmm... you shouldn't be here...")
    return False 

def generate_token(username):
    body = '{' \
              + '"admin": "' + "False" \
              + '", "username": "' + str(username) \
              + '"}'
    encoded = jwt.encode(json.loads(body), SECRET_KEY, algorithm='HS256')
    return encoded


if __name__ == "__main__":
    while True:
        choice = input("[?] Do you want to generate a token? (y/n): ")
        if choice == "n" or choice == "N":
            break
        username = input("[?] Enter your username: ")
        print("[+] Your token:", generate_token(username))
        choice = input("[?] Do you want to connect by a token? (y/n): ")
        if choice == "n" or choice == "N":
            break
        token = input("[?] Enter your token: ")
        if authorise(token):
            os.system("/bin/bash")
        else:
            print("Goodbye!")