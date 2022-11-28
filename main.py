import sqlite3
import pandas as pd
from datetime import date
import time

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

def show_info(user_id, cur):
    cur.execute(f"SELECT username, first_name, last_name, email, address, phone_number FROM users WHERE user_id = '{user_id}'")
    user_info = cur.fetchall()
    print("User Info:")
    print(f" Username: {user_info[0][0]}\n First Name: {user_info[0][1]}\n Last Name: {user_info[0][2]}\n Email: {user_info[0][3]}\n Address: {user_info[0][4]}\n Phone Number: {user_info[0][5]}\n ")


def edit(user_id, conn, cur):
    print("Here is a list of all column names:\nuser_id\nusername\npassword\nfirst_name\nlast_name\nemail\naddress\nphone_number")
    column = input("Select a column to edit => ")
    value = input("Enter a new value => ")
    query = f"UPDATE users SET {column} = '{value}' WHERE user_id='{user_id}'"
    try:
        cur.execute(query)
        print("Value Changed!")
    except:
        print("Invalid Column or Value")
        user_input = input("Would you like to try again? (y/n): ")
        while user_input != "y" and user_input != "n":
            print("Invalid input (y/n)")
            user_input = input("Would you like to try again? (y/n): ")
        if user_input == "y":
            edit(user_id, conn, cur)
    conn.commit()


def display_inventory(cur):
    cur.execute("SELECT * FROM inventory")
    inventory = cur.fetchall()
    for item in inventory:
        time.sleep(.25)
        print(f'{item[0]}: {item[1]} | ${item[2]}.00')


def add_to_cart(cur):
    conn = sqlite3.connect("cart.db")
    curs = conn.cursor()
    cart = pd.read_csv('data/cart.csv')
    cart.to_sql('cart', conn, if_exists='replace', index = False)
    conn.commit()
    add_another = ""

    while add_another != "n":
        id = input("Enter an Item ID: ")
        count = input("Enter the Quantity: ")
        cur.execute(f"SELECT price FROM inventory WHERE inventory_id = {id}")
        cost_data = cur.fetchall()
        cost = cost_data[0][0]
        curs.execute(f"INSERT INTO cart (inventory_id, cost, quantity) VALUES ({id}, {cost}, {count}) ")
        add_another = input("Would you like to add another item? (y/n) ")
        conn.commit()

    curs.execute("SELECT * FROM cart")
    cart = curs.fetchall()

    # Display cart

    for item in cart:
        cur.execute(f"SELECT name FROM inventory WHERE inventory_id = {item[0]}")
        name_data = cur.fetchall()
        name = name_data[0][0]
        print(f'{str(item[0])}: {name} | ${str(item[1])}.00 | {str(item[2])}')

    # Display total
    total = 0
    for item in cart:
        total+= int(item[1]) * int(item[2])
    print(f"Total: ${total}.00")
    return cart


def purchase(user_id, cart, conn, cur):
    d = date.today()
    today = d.strftime("%m/%d/%Y")

    for item in cart:
        cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES ({user_id}, {item[0]}, {item[1]}, {item[2]}, '{today}')")

    conn.commit()
    print("Purchase complete\n")
    # ADD LINE TO UPDATE COUNT IN INVENTORY

def view_purchases(user_id, cur):
    cur.execute(f"SELECT purchase_id, cost, quantity, dop FROM users INNER JOIN purchases ON users.user_id == purchases.user_id WHERE purchases.user_id == {user_id} ORDER BY dop")
    purchases = cur.fetchall()
    for purchase in purchases:
        cur.execute(f"SELECT name FROM inventory WHERE inventory_id = {purchase[2]}")
        name_data = cur.fetchall()
        name = name_data[0][0]
        print(f"{purchase[0]}: {name} | ${purchase[1]}.00 | {purchase[2]} | {purchase[3]}")


def view_inventory(cur):
    cur.execute(f'SELECT * FROM inventory')
    inventory = cur.fetchall()
    for item in inventory:
        print(f'{item[0]}: {item[1]} | ${item[2]}.00 | {item[3]}')

def edit_inventory(cur, conn):
    print("Enter an Inventory Id")
    id = input("=> ")
    print("Choose a section to edit\n1: Name\n2: Price\n3: Quantity")
    col = input("=> ")
    print("Enter a new value")
    val = input("=> ")
    try: 
        if col == "1":
            cur.execute(f"UPDATE inventory SET name = '{val}' WHERE inventory_id = {id}")
        elif col == "2":
            cur.execute(f"UPDATE inventory SET price = {val} WHERE inventory_id = {id}")
        elif col == "3":
            cur.execute(f"UPDATE inventory SET quantity = {val} WHERE inventory_id = {id}")
    except:
        print("Invalid input")
        user_input = input("Would you like to try again? (y/n): ")
        while user_input != "y" and user_input != "n":
            print("Invalid input (y/n)")
            user_input = input("Would you like to try again? (y/n): ")

        if user_input == "y":
            edit_inventory(conn, cur)
    conn.commit()

def view_all_purchases(cur):
    cur.execute("SELECT purchase_id, inventory_id, first_name, last_name, cost, quantity dop FROM purchases INNER JOIN users ON purchases.user_id == users.user_id")
    purchases = cur.fetchall()
    print(purchases)
    for purchase in purchases:
        cur.execute(f"SELECT name FROM inventory WHERE inventory_id = {purchase[1]}")
        name_data = cur.fetchall()
        name = name_data[0][0]
        print(f"{purchase[0]}: {purchase[2]} {purchase[3]} | {name} | {purchase[4]} | {purchase[5]}")

def view_users(cur):
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(users)
    for user in users:
        print(f"{user[0]}: {user[1]} {user[2]}\n username: {user[3]}\n email: {user[5]}\n address: {user[6]}\n phone number: {user[7]}")

def delete_user(cur, conn):
    print("Enter a user id to delete")   
    id = input("=> ")
    cur.execute(f"DELETE FROM users WHERE user_id == {id}")

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

                if user_input == "a":
                    view_inventory(cur)
                    print("Choose an option:\n a) Go Back\n b) Edit")
                    temp_input = input("=> ")
                    while temp_input != "b" and temp_input !="a":
                        temp_input = input("Invalid Input => ")
                    if temp_input == "b":
                        edit_inventory(cur, conn)
                
                elif user_input == "b":
                    view_all_purchases(cur)
                    print("Choose an option:\n a) Go Back")
                    temp_input = input("=> ")
                    while temp_input !="a":
                        temp_input = input("Invalid Input => ")
                
                elif user_input == "c":
                    view_users(cur)
                    print("Choose an option:\n a) Go Back\n b) Delete User")
                    temp_input = input("=> ")
                    while temp_input != "b" and temp_input !="a":
                        temp_input = input("Invalid Input => ")
                    if temp_input == "b":
                        delete_user(cur, conn)

                elif user_input == "d":
                    admin_mode = ""

                elif user_input == "e":
                    admin_mode = ""
                    quit = True

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