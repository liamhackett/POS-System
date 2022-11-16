import sqlite3
import pandas as pd

# Users
conn = sqlite3.connect("users.db")
cur = conn.cursor()
# users = pd.read_csv('data/users.csv')

# users.to_sql('users', conn, if_exists='replace', index = False)
try:   
    cur.execute("DROP TABLE users")
except:
    print("Creating Table")

cur.execute("CREATE TABLE users ( user_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, address TEXT NOT NULL, phone_number TEXT NOT NULL, admin INTEGER NOT NULL)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Liam', 'Hackett', 'lhackett', 'lhackett', 'wjhackett7@gmail.com', '39A Buell St', '802-393-2046', 1)")

conn.commit()

print("Created users table")
# Inventory 

inventory = pd.read_csv('data/inventory.csv')

inventory.to_sql('inventory', conn, if_exists='replace', index = False)
conn.commit()

print("Created inventory table")

# purchases

# purchases = pd.read_csv('data/purchases.csv')

# purchases.to_sql('purchases', conn, if_exists='replace', index = False)

try:   
    cur.execute("DROP TABLE purchases")
except:
    print("Creating Table")

cur.execute("CREATE TABLE purchases ( purchase_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, inventory_id INTEGER NOT NULL, cost INTEGER NOT NULL, quantity INTEGER NOT NULL, dop TEXT NOT NULL)")

conn.commit()

print("Created purchases table")

