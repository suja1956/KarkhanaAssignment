import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS Product (id integer PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price integer, image_url TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS CartItem (id integer PRIMARY KEY AUTOINCREMENT, product_id integer NOT NULL, quantity integer)')
print("Created table successfully!")

conn.close()