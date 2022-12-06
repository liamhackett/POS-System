
import sqlite3
import pandas as pd
from datetime import date
import time

# Allows user to view their account info
def show_info(user_id, cur):
    cur.execute(f"SELECT username, first_name, last_name, email, address, phone_number FROM users WHERE user_id = '{user_id}'")
    user_info = cur.fetchall()
    print("User Info:")
    print(f" Username: {user_info[0][0]}\n First Name: {user_info[0][1]}\n Last Name: {user_info[0][2]}\n Email: {user_info[0][3]}\n Address: {user_info[0][4]}\n Phone Number: {user_info[0][5]}\n ")


# Allows user to edit their account info
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


# Allows user to view the products available to purchase
def display_inventory(cur):
    cur.execute("SELECT * FROM inventory")
    inventory = cur.fetchall()
    for item in inventory:
        time.sleep(.25)
        print(f'{item[0]}: {item[1]} | ${item[2]}.00')

# Allows user to add an item to their cart
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


# Allows user to purchase the items in their cart
def purchase(user_id, cart, conn, cur):
    d = date.today()
    today = d.strftime("%m/%d/%Y")

    for item in cart:
        cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES ({user_id}, {item[0]}, {item[1]}, {item[2]}, '{today}')")
        cur.execute(f"SELECT quantity FROM inventory WHERE inventory_id = {item[0]}")
        quantity = cur.fetchall()
        cur.execute(f"UPDATE inventory SET quantity = {quantity[0][0]-1} WHERE inventory_id = {item[0]}")

    conn.commit()
    print("Purchase complete\n")

# allows user to view their purchases
def view_purchases(user_id, cur):
    cur.execute(f"SELECT purchase_id, cost, quantity, dop, inventory_id FROM users INNER JOIN purchases ON users.user_id == purchases.user_id WHERE purchases.user_id == {user_id} ORDER BY dop")
    purchases = cur.fetchall()
    for purchase in purchases:
        cur.execute(f"SELECT name FROM inventory WHERE inventory_id = {purchase[4]}")
        name_data = cur.fetchall()
        name = name_data[0][0]
        print(f"{purchase[0]}: {name} | ${purchase[1]}.00 | {purchase[2]} | {purchase[3]}")

