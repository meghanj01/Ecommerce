import sqlite3
from sqlite3 import Connection
from flask import abort, jsonify, make_response


class SQLiteConnection:
    def __init__(self, database_path, pool_size):
        self.database_path = database_path
        self.pool_size = pool_size
        self.connections = []

    def initialize_pool(self):
        for _ in range(self.pool_size):
            connection = sqlite3.connect(self.database_path, check_same_thread=False)
            connection.row_factory = sqlite3.Row
            self.connections.append(connection)

    def get_connection(self):
        if not self.connections:
            abort(make_response(jsonify(message="Connection exausted", status=500)))
        return self.connections.pop()

    def release_connection(self, connection: Connection):
        self.connections.append(connection)

    def close_all_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections.clear()


def initialize_connection():
    db_path = "./db_scripts/ecommerce.db"  # Replace with your SQLite database file path
    pool = SQLiteConnection(db_path, pool_size=5)
    pool.initialize_pool()
    return pool


def get_all_records(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        abort(make_response(jsonify(message=f"Error in get all records {e}")))
    finally:
        cursor.close()


def get_all_records_by_id(connection, query, id):
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        abort(make_response(jsonify(message=f"Error in get all records by ID {e}")))
    finally:
        cursor.close()


def check_record(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        connection.commit()
        return result
    except Exception as e:
        abort(make_response(jsonify(message=f"Error in ckeck  records {e}")))
    finally:
        cursor.close()


def record_by_id(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, (params,))
        result = cursor.fetchone()
        connection.commit()
        return result
    except Exception as e:
        abort(make_response(jsonify(message=f"Error in get  records by ID {e}")))
    finally:
        cursor.close()


def post_record(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, tuple(params.values()))
        result = cursor.lastrowid
        connection.commit()
        return result
    except Exception as e:
        abort(make_response(jsonify(message=f"Error in post records {e}")))
    finally:
        cursor.close()


def update_record(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, tuple(params.values()))
        connection.commit()
        return
    except sqlite3.Error as e:
        abort(make_response(jsonify(message=f"Error in update records {e}")))
    finally:
        cursor.close()
