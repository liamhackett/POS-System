import sqlite3
import pandas as pd

# Users
conn = sqlite3.connect("users.db")

users = pd.read_csv('data/users.csv')

users.to_sql('users', conn, if_exists='replace', index = False)

conn.commit()

print("Created users table")
# Inventory 

posts = pd.read_csv('data/inventory.csv')

posts.to_sql('inventory', conn, if_exists='replace', index = False)
conn.commit()

print("Created inventory table")

# purchases

followers = pd.read_csv('data/purchases.csv')

followers.to_sql('purchases', conn, if_exists='replace', index = False)
conn.commit()

print("Created purchases table")
