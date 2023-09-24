from ..db import (
    post_record,
    get_all_records,
    update_record,
    record_by_id,
    check_record,
)
from flask import Flask, abort, make_response, jsonify


def insert_product(conn, data):
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
    query = """ select * from products"""
    result = get_all_records(conn, query)
    if result:
        return result
    else:
        abort(make_response(jsonify(messgae="product table is empty", message=400)))


def check_product_id(conn, id):
    query = """ select id from products where id = ?"""
    (result,) = record_by_id(conn, query, id)
    if result:
        return
    else:
        abort(make_response(jsonify(message="product doesnot exists", status=404)))


def update_product(conn, req):
    query = """update products set name = ?, description = ?, price = ? ,inventory_quantity = ? where id = ? """
    update_record(conn, query, req)
    return


def delete_product(conn, req):
    query = """delete from products where id = ? """
    record_by_id(conn, query, req)
    return


def get_product_by_id(conn, id):
    query = """select name, description, price, inventory_quantity from products where id = ?"""
    result = record_by_id(conn, query, id)
    if result and len(result) > 0:
        return result
    abort(make_response(jsonify(message="Product not found", status=404)))


def check_product_quantity(conn, data):
    query = """ select 1 from products where id = ? and inventory_quantity >= ?"""
    result = check_record(conn, query, data)
    if result:
        (result,) = result
        return result
    abort(make_response(jsonify(message="Product quantity is exceeding", status=400)))
