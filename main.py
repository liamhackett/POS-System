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

    return logged_in, username
   
def show_info(user_id, cur):
    cur.execute(f"SELECT username, first_name, last_name, email, address, phone_number FROM users WHERE user_id = '{user_id}'")
    user_info = cur.fetchall()
    print("User Info:")
    print(f" Username: {user_info[0][0]}\n First Name: {user_info[0][1]}\n Last Name: {user_info[0][2]}\n Email: {user_info[0][3]}\n Address: {user_info[0][4]}\n Phone Number: {user_info[0][5]}\n ")


def main():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    logged_in, username = login(cur)
    user_input = ""
    quit = False

    if logged_in:
        print("Successful Login")
        
        cur.execute(f"SELECT 'First Name', 'Last Name', user_id FROM users WHERE username = '{username}'")
        name = cur.fetchall()
        user_id = name[0][2]

        while not quit:
            print("Welcome to POS System")
            print("Choose an Option:\na) View Products\nb) User Info\nc) Log-out")
            user_input =  input("=> ")
            while user_input != "a" and user_input !="b" and user_input != "c":
                print("Invalid Input")
                user_input =  input("=> ")

            if user_input == "a":
                print("Inventory")
            elif user_input == "b":
                show_info(user_id, cur)
            elif user_input == "c":
                quit = True


    
    



main()