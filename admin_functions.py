import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    for purchase in purchases:
        cur.execute(f"SELECT name FROM inventory WHERE inventory_id = {purchase[1]}")
        name_data = cur.fetchall()
        name = name_data[0][0]
        print(f"{purchase[0]}: {purchase[2]} {purchase[3]} | {name} | {purchase[4]} | {purchase[5]}")


def view_users(cur):
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    for user in users:
        print(f"{user[0]}: {user[1]} {user[2]}\n username: {user[3]}\n email: {user[5]}\n address: {user[6]}\n phone number: {user[7]}")


def delete_user(cur, conn):
    print("Enter a user id to delete")   
    id = input("=> ")
    cur.execute(f"DELETE FROM users WHERE user_id == {id}")


def create_admin(cur, conn):
    print("Enter a User Id to make admin")
    cur.execute("SELECT count(user_id) FROM users")
    num = cur.fetchall()
    print(num)
    id = input("=> ")
    if  int(id) >= int(num[0][0]):
        print("HERE")
    while(id.isdigit() != True or int(id) >= int(num[0][0])):
        print("Invalid input. Must be an integer and be a valid user id")
        id = input("=> ")
    
    cur.execute(f"UPDATE users SET admin = 1 WHERE user_id = {id}")
    conn.commit()


def average_purchases(cur):
    cur.execute(f"SELECT AVG(cost * quantity) FROM purchases")
    avg = cur.fetchall()
    print(f"Average Cost of Purchases: {avg[0][0]}")


def graph_purchases(conn):
    dataframe = pd.read_sql("SELECT count(dop) as sales, dop FROM purchases GROUP BY dop;", conn)
    print(dataframe.head())
    plt.figure(figsize=(50, 5))
    sns.lineplot(x="dop", y="sales", data=dataframe).set_title("Sales")
    sns.set(font_scale=.5)
    plt.show()


def graph_inventory(conn):
    dataframe = pd.read_sql("SELECT name, quantity FROM inventory", conn)
    print(dataframe.head())
    plt.figure(figsize=(50, 5))
    sns.barplot(x = "quantity", y = "name", data = dataframe)
    sns.set(font_scale=.5)
    plt.show()


def  min_max_items(cur):
    print("Choose an Option:\n a) Max\n b) Min")
    choice = input("=>")
    func = ""
    while choice != "a" and choice != "b":
        print("Invalid Input")
        choice = input("=> ")
    print("Choose and Option:\n a) Cost\n b) Quantity")
    numeric = input("=> ")
    while numeric != "a" and numeric != "b":
        print("Invalid Input")
        choice = input("=> ")
    if choice == "a":
        func = "Max"
    elif choice == "b":
        func = "Min"
    if numeric == "a":
        numeric = "price"
    elif numeric == "b":
        numeric = "quantity"

    cur.execute(f"SELECT {func}({numeric}) FROM inventory;")
    results = cur.fetchall()
    print(f"The {func} {numeric} of items is {results[0][0]}")