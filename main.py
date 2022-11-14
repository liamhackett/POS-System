import sqlite3
import pandas as pd

def login(cur):
    username = ""
    password = ""
    logged_in = False

    while not logged_in:
        username = input("Username: ").lower()
        password = input("Password: ")
        
        cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE username = '{username}' AND password = '{password}')")
        found = cur.fetchall()

        if found[0][0] == 1:
            logged_in = True
        else:
            cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE username = '{username}')")
            usr_found = cur.fetchall()
            if usr_found[0][0] == 0:
                print("User not found")
            else:
                print("Access denied")

    return logged_in





def main():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    logged_in = login(cur)
    if logged_in:
        print("Successful Login")
    
    



main()