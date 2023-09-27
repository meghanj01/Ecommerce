from ..db import record_by_id, post_record, get_all_records, update_record
from flask import abort, make_response, jsonify


def is_admin(conn, id):
    """
    Check if a user is an admin based on their ID.

    Args:
        conn: Database connection.
        id (int): User ID.

    Returns:
        None: If the user is an admin.
        Raises:
            HTTPException: If the user is not an admin.
    """
    query = """select is_admin from users where id = ?"""
    (result,) = record_by_id(conn, query, id)
    if result == 1:
        return
    abort(make_response(jsonify(message="User is not admin", status=400)))


def insert_user(conn, data):
    """
    Insert a new user record into the database.

    Args:
        conn: Database connection.
        data (dict): User data including username, password, email, and is_admin.

    Returns:
        int: The ID of the inserted user.
        Raises:
            HTTPException: If insertion fails.
    """
    query = """ INSERT INTO users (username, password, email, is_admin)
    VALUES (?,?,?,?)"""
    (result,) = post_record(conn, query, data)
    if result:
        return result
    abort(make_response(jsonify(message="Unable to insert record", status=400)))


def get_all_users(conn):
    """
    Get a list of all users from the database.

    Args:
        conn: Database connection.

    Returns:
        list: List of user records.
        Raises:
            HTTPException: If no user records exist.
    """
    query = """ select username, password, email, is_admin from users"""
    result = get_all_records(conn, query)
    if result:
        return result
    abort(make_response(jsonify(message="users record does not exists", status=400)))


def check_user_id(conn, id):
    """
    Check if a user with the specified ID exists in the database.

    Args:
        conn: Database connection.
        id (int): User ID.

    Returns:
        None: If the user with the given ID exists.
        Raises:
            HTTPException: If the user with the given ID does not exist.
    """
    query = """select id from users where id = ?"""
    result = record_by_id(conn, query, id)
    if result:
        return
    else:
        abort(make_response(jsonify(message="user doesnot exists", status=404)))


def update_user(conn, req):
    """
    Update user information in the database.

    Args:
        conn: Database connection.
        req (dict): User data to be updated including username, password, email, is_admin, and user ID.

    Returns:
        None
    """
    query = """update users set username = ?, password = ?, email = ? ,is_admin = ? where id = ? """
    update_record(conn, query, req)
    return


def delete_user(conn, req):
    """
    Delete a user from the database.

    Args:
        conn: Database connection.
        req (int): User ID to be deleted.

    Returns:
        None
    """
    query = """delete from users where id = ? """
    record_by_id(conn, query, req)
    return


def get_user_by_id(conn, id):
    """
    Get user information by their ID from the database.

    Args:
        conn: Database connection.
        id (int): User ID.

    Returns:
        dict: User information including username, email, and is_admin.
        Raises:
            HTTPException: If the user with the given ID does not exist.
    """
    query = """select username, email, is_admin from users where id = ?"""
    result = record_by_id(conn, query, id)
    if result and len(result) > 0:
        return result
    abort(make_response(jsonify(message="User not found", status=404)))
