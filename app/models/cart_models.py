from ..db import (
    record_by_id,
    post_record,
    get_all_records,
    update_record,
    get_all_records_by_id,
)
from flask import abort, make_response, jsonify


def insert_cart(conn, user_id):
    """
    Insert a cart for a user into the database.

    Args:
        conn: Database connection.
        user_id (int): User ID for whom the cart is created.

    Returns:
        None
        Raises:
            HTTPException: If cart creation fails.
    """
    query = """
            INSERT INTO carts (user_id)
            VALUES (?);
            """
    (result,) = record_by_id(conn, query, user_id)
    if result:
        return
    else:
        abort(
            make_response(jsonify(message="Unable to create cart for user", status=404))
        )


def insert_cart_products(conn, data):
    """
    Insert cart items into the database.

    Args:
        conn: Database connection.
        data (list): List of cart item data, each containing product_id and quantity.

    Returns:
        None
        Raises:
            HTTPException: If insertion fails.
    """
    query = """
            INSERT INTO cart_items (cart_id, product_id, quantity)
            VALUES ((select id from carts where user_id = ?),?,?);
            """
    result = post_record(conn, query, data)
    if result:
        return
    else:
        abort(make_response(jsonify(messgae="cart items is not inserted", message=400)))


def update_cart_products(conn, data):
    """
    Update cart item quantity in the database.

    Args:
        conn: Database connection.
        data (dict): Data containing quantity, user_id, and product_id.

    Returns:
        None
    """
    query = """UPDATE cart_items
            SET quantity = ?
            WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ?)
            AND product_id = ?;"""
    update_record(conn, query, data)
    return


def get_cart_by_user_id(conn, id):
    """
    Get cart items by user ID from the database.

    Args:
        conn: Database connection.
        id (int): User ID for whom the cart items are retrieved.

    Returns:
        list: List of cart items containing product ID, product name, quantity, and price.
        Raises:
            HTTPException: If no cart items exist for the user.
    """
    query = """select p.id, p.name, ci.quantity, p.price
        from cart_items ci
        join products p on ci.product_id = p.id
        join carts c on ci.cart_id = c.id
        where c.user_id = ?"""
    result = get_all_records_by_id(conn, query, id)
    if result and len(result) > 0:
        return result
    abort(make_response(jsonify(message="items not found", status=404)))


def delete_cart_item(conn, data):
    """
    Delete a cart item from the database.

    Args:
        conn: Database connection.
        data (dict): Data containing user_id and product_id.

    Returns:
        None
    """
    query = """
        DELETE FROM cart_items
        WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ?)
        AND product_id = ?;"""
    update_record(conn, query, data)
    return


def delete_cart(conn, id):
    """
    Delete all cart items for a user from the database.

    Args:
        conn: Database connection.
        id (int): User ID for whom the cart is deleted.

    Returns:
        None
    """
    query = """DELETE FROM cart_items
                WHERE cart_id IN (SELECT id FROM carts WHERE user_id = ?);"""
    record_by_id(conn, query, id)
    return
