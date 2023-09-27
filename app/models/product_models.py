from ..db import (
    post_record,
    get_all_records,
    update_record,
    record_by_id,
    check_record,
)
from flask import Flask, abort, make_response, jsonify


def insert_product(conn, data):
    """
    Insert a new product into the database.

    Args:
        conn: Database connection.
        data (dict): Product data including name, description, price, and inventory_quantity.

    Returns:
        None
        Raises:
            HTTPException: If insertion fails.
    """
    query = """
            INSERT INTO products (name, description, price, inventory_quantity)
            VALUES (?,?,?,?);
            """
    result = post_record(conn, query, data)
    if result:
        return
    else:
        abort(make_response(jsonify(messgae="Product is not inserted", message=400)))


def get_all_products(conn):
    """
    Get a list of all products from the database.

    Args:
        conn: Database connection.

    Returns:
        list: List of product records.
        Raises:
            HTTPException: If no product records exist.
    """
    query = """ select * from products"""
    result = get_all_records(conn, query)
    if result:
        return result
    else:
        abort(make_response(jsonify(messgae="product table is empty", message=400)))


def check_product_id(conn, id):
    """
    Check if a product with the specified ID exists in the database.

    Args:
        conn: Database connection.
        id (int): Product ID.

    Returns:
        None: If the product with the given ID exists.
        Raises:
            HTTPException: If the product with the given ID does not exist.
    """
    query = """ select id from products where id = ?"""
    (result,) = record_by_id(conn, query, id)
    if result:
        return
    else:
        abort(make_response(jsonify(message="product doesnot exists", status=404)))


def update_product(conn, req):
    """
    Update product information in the database.

    Args:
        conn: Database connection.
        req (dict): Product data to be updated including name, description, price, inventory_quantity, and product ID.

    Returns:
        None
    """
    query = """update products set name = ?, description = ?, price = ? ,inventory_quantity = ? where id = ? """
    update_record(conn, query, req)
    return


def delete_product(conn, req):
    """
    Delete a product from the database.

    Args:
        conn: Database connection.
        req (int): Product ID to be deleted.

    Returns:
        None
    """
    query = """delete from products where id = ? """
    record_by_id(conn, query, req)
    return


def get_product_by_id(conn, id):
    """
    Get product information by its ID from the database.

    Args:
        conn: Database connection.
        id (int): Product ID.

    Returns:
        dict: Product information including name, description, price, and inventory_quantity.
        Raises:
            HTTPException: If the product with the given ID does not exist.
    """
    query = """select name, description, price, inventory_quantity from products where id = ?"""
    result = record_by_id(conn, query, id)
    if result and len(result) > 0:
        return result
    abort(make_response(jsonify(message="Product not found", status=404)))


def check_product_quantity(conn, data):
    """
    Check if the quantity of a product is available in the inventory.

    Args:
        conn: Database connection.
        data (tuple): Product ID and desired quantity.

    Returns:
        None: If the quantity is available.
        Raises:
            HTTPException: If the product quantity is insufficient.
    """
    query = """ select 1 from products where id = ? and inventory_quantity >= ?"""
    result = check_record(conn, query, data)
    if result:
        (result,) = result
        return result
    abort(make_response(jsonify(message="Product quantity is exceeding", status=400)))
