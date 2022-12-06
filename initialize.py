import sqlite3
import pandas as pd

# Users
conn = sqlite3.connect("users.db")
cur = conn.cursor()

try:   
    cur.execute("DROP TABLE users")
except:
    print("Creating Table")

cur.execute("CREATE TABLE users ( user_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, address TEXT NOT NULL, phone_number TEXT NOT NULL, admin INTEGER NOT NULL)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Liam', 'Hackett', 'lhackett', 'lhackett', 'wjhackett7@gmail.com', '39A Buell St', '802-393-2046', 1)")
# Add fabricated user data
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('John', 'Smith', 'jsmith', 'jsmith', 'jsmith@gmail.com', '1 Main St', '802-111-1111', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Jane', 'Doe', 'jdoe', 'jdoe', 'jdoe@gmail.com', '2 Main st', '802-123-1234', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Example', 'User', 'exam', 'exam', 'example@gmail.com', '3 Main st', '802-123-1235', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Peter', 'Parker', 'spiderman', 'spidey', 'spiderman@gmail.com', '4 Main st', '802-123-1236', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Clark', 'Kent', 'superman', 'superman', 'superman@gmail.com', '5 Main st', '802-123-1237', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Lois', 'Lane', 'lane', 'lane', 'llane@gmail.com', '6 Main st', '802-123-1238', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Bruce', 'Wayne', 'bwayne', 'batman', 'batman@gmail.com', '7 Main st', '802-123-1239', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Barry', 'Allen', 'barry', 'flash', 'flash@gmail.com', '8 Main st', '802-123-1230', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('first', 'last', 'test', 'test', 'test@gmail.com', '9 Main st', '802-123-1244', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Larry', 'Bird', 'lbird33', 'lbird33', 'lbird33@gmail.com', '10 Main st', '802-123-1254', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Michael', 'Jordan', 'mj23', 'mj23', 'mj23@gmail.com', '11 Main st', '802-123-1264', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Lebron', 'James', 'kingjames23', 'kingjames23', 'kingjames23@gmail.com', '12 Main st', '802-123-1274', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Damian', 'Lillard', 'dame', 'dolla', 'dolla0@gmail.com', '13 Main st', '802-123-1284', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Zion', 'Williamson', 'zion', 'zion', 'zion@gmail.com', '14 Main st', '802-123-1294', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Kevin', 'Durant', 'easymoneysniper', 'kd', 'kd@gmail.com', '15 Main st', '802-123-1204', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Kendrick', 'Lamar', 'kdot', 'kdot', 'kdot@gmail.com', '16 Main st', '802-123-1334', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Jermaine', 'Cole', 'jcole', 'jcole', 'jcole@gmail.com', '17 Main st', '802-123-1434', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('New', 'User', 'user', 'user', 'user@gmail.com', '18 Main st', '802-123-1534', 0)")
cur.execute("INSERT INTO users (first_name, last_name, username, password, email, address, phone_number, admin) VALUES ('Newer', 'User', 'user1', 'user1', 'user1@gmail.com', '19 Main st', '802-123-1634', 0)")










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
# Add Fabricated Purchases
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (2, 3, 300, 1, '11/01/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 4, 250, 1, '11/02/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (3, 5, 20, 1, '11/07/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 6, 25, 1, '11/07/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 7, 100, 1, '11/07/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (2, 8, 25, 1, '11/07/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (2, 9, 20, 1, '11/07/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (2, 10, 100, 1, '11/08/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (3, 11, 350, 1, '11/09/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (3, 12, 300, 1, '11/10/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 13, 50, 1, '11/11/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 14, 30, 1, '11/12/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (3, 15, 35, 1, '11/13/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 16, 25, 1, '11/14/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 17, 25, 1, '11/15/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 18, 30, 1, '11/15/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 19, 100, 1, '11/16/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (2, 20, 25, 1, '11/18/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 1, 1000, 1, '11/19/22')")
cur.execute(f"INSERT INTO purchases (user_id, inventory_id, cost, quantity, dop) VALUES (1, 2, 500, 1, '11/20/22')")


























conn.commit()

print("Created purchases table")

