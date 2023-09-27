from ..db import (
    record_by_id,
    post_record,
    get_all_records,
    update_record,
    get_all_records_by_id,
    check_record,
)
from flask import abort, make_response, jsonify


def insert_order_products(conn, data, id):
    """
    Insert order products into the database.

    Args:
        conn: Database connection.
        data (list): List of order product data, each containing product_id and quantity.
        id (int): User ID for whom the order is placed.

    Returns:
        None
        Raises:
            HTTPException: If insertion fails.
    """
    query = "INSERT into orders (user_id, order_date) VALUES (?, CURRENT_TIMESTAMP)"

    result = post_record(conn, query, {"id": id})
    if not result:
        abort(make_response(jsonify(message=" unable to place order", status=500)))
    query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES"
    params = []
    formatter = []
    for d in data:
        formatter.append("(?,?,?)")
        params.extend((result, d["product_id"], d["quantity"]))
    formatter = ",".join(formatter)
    query += formatter
    check_record(conn, query, tuple(params))
    return


def get_order_by_user_id(conn, id):
    """
    Get orders by user ID from the database.

    Args:
        conn: Database connection.
        id (int): User ID for whom the orders are retrieved.

    Returns:
        list: List of order records containing product_id, quantity, product name, product price, and order_id.
        Raises:
            HTTPException: If no orders exist for the user.
    """
    query = """
        SELECT ot.product_id, ot.quantity ,p.name, p.price, ot.order_id from order_items ot
        JOIN orders o on ot.order_id = o.id
        JOIN products p on ot.product_id = p.id
        where o.user_id = ?"""
    result = get_all_records_by_id(conn, query, id)
    if not result:
        abort(make_response(jsonify(message="Order was not placed sorry", status=500)))
    return result


def delete_order_item(conn, data):
    """
    Delete an order item from the database.

    Args:
        conn: Database connection.
        data (dict): Data containing order_id and user_id.

    Returns:
        None
    """
    query = """
        DELETE FROM order 
        WHERE id = ? and user_id = ?"""
    update_record(conn, query, data)
    return
