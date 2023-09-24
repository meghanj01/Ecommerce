from ..db import record_by_id, post_record, get_all_records, update_record
from flask import abort, make_response, jsonify


def is_admin(conn, id):
    query = """select is_admin from users where id = ?"""
    (result,) = record_by_id(conn, query, id)
    if result == 1:
        return
    abort(make_response(jsonify(message="User is not admin", status=400)))


def insert_user(conn, data):
    query = """ INSERT INTO users (username, password, email, is_admin)
    VALUES (?,?,?,?)"""
    (result,) = post_record(conn, query, data)
    if result:
        return result
    abort(make_response(jsonify(message="Unable to insert record", status=400)))


def get_all_users(conn):
    query = """ select username, password, email, is_admin from users"""
    result = get_all_records(conn, query)
    if result:
        return result
    abort(make_response(jsonify(message="users record does not exists", status=400)))


def check_user_id(conn, id):
    query = """select id from users where id = ?"""
    result = record_by_id(conn, query, id)
    if result:
        return
    else:
        abort(make_response(jsonify(message="user doesnot exists", status=404)))


def update_user(conn, req):
    query = """update users set username = ?, password = ?, email = ? ,is_admin = ? where id = ? """
    update_record(conn, query, req)
    return


def delete_user(conn, req):
    query = """delete from users where id = ? """
    record_by_id(conn, query, req)
    return


def get_user_by_id(conn, id):
    query = """select username, email, is_admin from users where id = ?"""
    result = record_by_id(conn, query, id)
    if result and len(result) > 0:
        return result
    abort(make_response(jsonify(message="User not found", status=404)))
