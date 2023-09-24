import sqlite3


connection = sqlite3.connect("ecommerce.db")

try:
    with open("create_scripts.sql") as f:
        connection.executescript(f.read())
    cur = connection.cursor()

    #  Insert data into the 'users' table
    cur.execute(
        """INSERT INTO users (username, password, email, is_admin)
    VALUES
        ('user1', 'hashed_password1', 'user1@example.com', FALSE),
        ('admin', 'hashed_admin_password', 'admin@example.com', TRUE);"""
    )

    #  Insert data into the 'products' table
    cur.execute(
        """INSERT INTO products (name, description, price, inventory_quantity)
    VALUES
        ('Product 1', 'Description for Product 1', 19.99, 100),
        ('Product 2', 'Description for Product 2', 29.99, 50),
        ('Product 3', 'Description for Product 3', 9.99, 200);"""
    )

    #  Insert data into the 'carts' table (assuming cart IDs are auto-generated)
    cur.execute(
        """INSERT INTO carts (user_id)
    VALUES
        (1),
        (1);"""
    )

    #  Insert data into the 'orders' table (assuming order IDs are auto-generated)
    # cur.execute(
    #     """INSERT INTO orders (user_id, order_date)
    # VALUES
    #     (1, '2023-09-23 10:00:00'),
    #     (1, '2023-09-24 15:30:00');"""
    # )

    #  Insert data into the 'cart_items' table
    cur.execute(
        """INSERT INTO cart_items (cart_id, product_id, quantity)
    VALUES
        (1, 1, 2),
        (2, 2, 3);"""
    )

    # Insert data into the 'order_items' table
    # cur.execute(
    #     """INSERT INTO order_items (order_id, product_id, quantity)
    # VALUES
    #     (1, 1, 2),
    #     (1, 2, 1),
    #     (2, 3, 5);"""
    # )

    # commit the changes
    connection.commit()
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
