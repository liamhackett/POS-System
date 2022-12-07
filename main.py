import sqlite3
from admin_functions import *
from user_functions import *


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


def create_account(conn, cur):
    print("Create Account")
    username = input("Username: ")
    password = input("Password: ")
    password2 = input("Confirm Password: ")
    while password != password2:
        print("Passwords do not match")
        password = input("Password: ")
        password2 = input("Confirm Password: ")
    
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email Address: ")
    address = input("Address: ")
    phone_number = input("Phone Number: ")
    try:
        cur.execute(f"INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('{first_name}', '{last_name}', '{username}', '{password}', '{email}', '{address}', '{phone_number}', 0)")
    except:
        print("Error")
    conn.commit()

    print("User Created")


def main():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    account = input("Do you have an account? (y/n): ")
    while account != "y" and account != "n":
        account = input("Invalid Input (y/n): ")
    if account == "n":
        create_account(conn, cur)

    logged_in, username = login(cur)
    user_input = ""
    quit = False
    
    if logged_in:
        print("Successful Login")
        
        cur.execute(f"SELECT first_name, last_name, user_id, admin FROM users WHERE username = '{username}'")
        name = cur.fetchall()
        user_id = name[0][2]
        admin = name[0][3]
        
        # Admin mode options
        if admin == 1:
            admin_mode = input("Would you like to enter Admin mode? (y/n): ")
            while admin_mode != "y" and admin_mode != "n":
                print("Invalid Input")
                admin_mode = input("=> ")
            while admin_mode == "y":
                print("Admin mode")
                print("Choose an Option:\na) View Inventory\nb) View Purchases\nc) View Users\nd) Enter Customer Mode\ne) Log-out")
                user_input =  input("=> ")
                while user_input != "a" and user_input !="b" and user_input != "c" and user_input != "d" and user_input != "e":
                    print("Invalid Input")
                    user_input =  input("=> ")
                
                # Admin view inventory
                if user_input == "a":
                    view_inventory(cur)
                    print("Choose an option:\n a) Go Back\n b) Edit\n c) Visualize Inventory\n d) Min/Max of Items")
                    temp_input = input("=> ")
                    while temp_input != "b" and temp_input !="a" and temp_input != "c" and temp_input != "d":
                        temp_input = input("Invalid Input => ")
                    if temp_input == "b":
                        edit_inventory(cur, conn)
                    elif temp_input == "c":
                        graph_inventory(conn)
                    elif temp_input == "d":
                        min_max_items(cur)
                # Admin View Purchases
                elif user_input == "b":
                    view_all_purchases(cur)
                    print("Choose an option:\n a) Go Back\n b) Average Cost of Purchases\n c) Graph Sales")
                    temp_input = input("=> ")
                    while temp_input !="a" and temp_input !="b" and temp_input !="c":
                        temp_input = input("Invalid Input => ")
                    if temp_input == "b":
                        average_purchases(cur)
                    elif temp_input == "c":
                        graph_purchases(conn)

                # Admin View Users
                elif user_input == "c":
                    view_users(cur)
                    print("Choose an option:\n a) Go Back\n b) Delete User\n c) Create New Admin")
                    temp_input = input("=> ")
                    while temp_input != "b" and temp_input !="a" and temp_input != "c":
                        temp_input = input("Invalid Input => ")
                    if temp_input == "b":
                        delete_user(cur, conn)
                    if temp_input == "c":
                        create_admin(cur, conn)

                # Enter Customer Mode
                elif user_input == "d":
                    admin_mode = ""

                # Log-Out
                elif user_input == "e":
                    admin_mode = ""
                    quit = True

        # Customer options
        while not quit:
            print("Welcome to POS System")
            print("Choose an Option:\na) View Products\nb) User Info\nc) View Purchases\nd) Log-out")
            user_input =  input("=> ")
            while user_input != "a" and user_input !="b" and user_input != "c" and user_input != "d":
                print("Invalid Input")
                user_input =  input("=> ")

            # View Products
            if user_input == "a":
                print("Inventory")
                display_inventory(cur)
                print("Choose an option:\n a) Go Back\n b) Add to Cart")
                temp_input = input("=> ")
                while temp_input != "b" and temp_input !="a" and temp_input !="c":
                    temp_input = input("Invalid Input => ")
                if temp_input == "b":
                    cart = add_to_cart(cur)
                    purch = input("Purchase (y/n): ")
                    while purch != "y" and purch != "n":
                        print("Invalid Input")
                        purch = input("Purchase (y/n): ")
                    if purch == "y":
                        purchase(user_id, cart, conn, cur)

            # User Info
            elif user_input == "b":
                show_info(user_id, cur)
                print("Choose an option:\n a) Go Back\n b) Edit")
                temp_input = input("=> ")
                while temp_input != "b" and temp_input !="a":
                    temp_input = input("Invalid Input => ")
                if temp_input == "b":
                    edit(user_id, conn, cur)
            
            # View Purchases
            elif user_input == "c":
                view_purchases(user_id, cur)

            # Log out
            elif user_input == "d":
                quit = True


main()