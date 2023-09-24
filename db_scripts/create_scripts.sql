-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS products;
-- DROP TABLE IF EXISTS carts;
-- DROP TABLE IF EXISTS cart_items; 
-- DROP TABLE IF EXISTS order_items; 

-- Create the 'users' table
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username VARCHAR(20) NOT NULL UNIQUE,
password VARCHAR(20) NOT NULL,
email VARCHAR(20) NOT NULL UNIQUE,
is_admin BOOLEAN DEFAULT FALSE
);

-- Create the 'products' table
-- numeric(10,2) is a number that has 8 digits before the decimal and 2 digits after the decimal.
CREATE TABLE products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(20) NOT NULL UNIQUE,
description TEXT,
price NUMERIC(10,2) NOT NULL,
inventory_quantity INTEGER NOT NULL
);

-- Create the 'carts' table
CREATE TABLE carts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL ,
CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the 'orders' table
CREATE TABLE orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
order_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the 'cart_items' table for the many-to-many relationship between Cart and Product
CREATE TABLE cart_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
cart_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
quantity INTEGER NOT NULL,
CONSTRAINT fk_cart_id FOREIGN KEY (cart_id) REFERENCES carts(id),
CONSTRAINT fk_products_id FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Create the 'order_items' table for the many-to-many relationship between Order and Product
CREATE TABLE order_items(
id INTEGER PRIMARY KEY AUTOINCREMENT,
order_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
quantity INTEGER NOT NULL,
CONSTRAINT fk_order_id FOREIGN KEY (order_id) REFERENCES orders(id),
CONSTRAINT fk_products_id FOREIGN KEY (product_id) REFERENCES products(id)
);