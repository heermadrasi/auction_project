import mysql.connector

# CONNECT TO MYSQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="heer1510"
)

cursor = db.cursor(buffered=True)

# CREATE DATABASE
cursor.execute("CREATE DATABASE IF NOT EXISTS auction_db")
cursor.execute("USE auction_db")

# ======================
# CREATE 8 TABLES
# ======================

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    starting_price INT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bids (
    bid_id INT AUTO_INCREMENT PRIMARY KEY,
    amount INT,
    user_id INT,
    item_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS item_category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    category_id INT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS watchlist (
    watch_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS auctions (
    auction_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    start_time DATETIME,
    end_time DATETIME,
    FOREIGN KEY (item_id) REFERENCES items(item_id)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT,
    amount INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
)""")

print("Database and tables created successfully!")