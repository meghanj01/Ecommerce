from flask import Flask, jsonify, request, Blueprint, g
from .validations import validate_post_products, validate_post_users
from .models.product_models import (
    insert_product,
    get_all_products,
    check_product_id,
    update_product,
    get_product_by_id,
    delete_product,
    check_product_quantity,
)
from .models.users_model import (
    is_admin,
    insert_user,
    get_all_users,
    delete_user,
    get_user_by_id,
    check_user_id,
    update_user,
)
from .models.cart_models import (
    insert_cart,
    insert_cart_products,
    update_cart_products,
    get_cart_by_user_id,
    delete_cart_item,
    delete_cart,
)
from .models.order_models import (
    insert_order_products,
    get_order_by_user_id,
    delete_order_item,
)
from .convertor import encrypt_password

# create a flask blueprint
ecommerce = Blueprint("ecommerce", __name__)


@ecommerce.route("/products", methods=["GET", "POST"])
def products_list():
    conn = g.db_connection
    if request.method == "POST":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = {
            "product_name": data.get("product_name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "product_quantity": data.get("quantity"),
        }
        validate_post_products(req)
        insert_product(conn, req)
    products = get_all_products(conn)
    product_list = []
    for product in products:
        product_list.append(
            {
                "product_name": product["name"],
                "product_equantity": product["inventory_quantity"],
                "description": product["description"],
                "price": product["price"],
            }
        )
    return jsonify(message=product_list, status=200)


@ecommerce.route("/products/<int:id>", methods=["GET", "PUT", "DELETE"])
def products_by_id(id):
    conn = g.db_connection
    if request.method == "PUT":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = {
            "product_name": data.get("product_name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "product_quantity": data.get("quantity"),
        }
        check_product_id(conn, id)
        req["id"] = id
        validate_post_products(req)
        update_product(conn, req)
        return jsonify(message=f"product id :{id} successfully updated", status=200)
    elif request.method == "GET":
        product = get_product_by_id(conn, id)
        result = {
            "product_name": product["name"],
            "product_equantity": product["inventory_quantity"],
            "description": product["description"],
            "price": product["price"],
        }
        return jsonify(message=result, status=200)
    elif request.method == "DELETE":
        delete_product(conn, id)
        return jsonify(message=f"Product id: {id} is deleted successfully", status=200)


@ecommerce.route("/users/admin/<int:id>", methods=["GET"])
def get_users_admin(id):
    conn = g.db_connection
    is_admin(conn, id)
    users = get_all_users(conn)
    users_list = []
    for user in users:
        users_list.append(
            {
                "user_name": user["username"],
                "email": user["email"],
                "is_admin": user["is_admin"],
            }
        )
    return jsonify(message=users_list, status=200)


@ecommerce.route("/users/", methods=["POST"])
def post_users():
    conn = g.db_connection
    if not request.is_json:
        return jsonify(message="Data is not in json format", status=400)
    data = request.get_json()
    req = {
        "user_name": data.get("user_name"),
        "password": data.get("password"),
        "email": data.get("email"),
        "is_admin": data.get("is_admin"),
    }

    validate_post_users(req)
    req["password"] = encrypt_password(req["password"])
    user_id = insert_user(conn, req)
    insert_cart(conn, user_id)
    return jsonify(message="user is added successfully", status=200)


@ecommerce.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def users_by_id(id):
    conn = g.db_connection
    if request.method == "PUT":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = {
            "user_name": data.get("user_name"),
            "password": data.get("password"),
            "email": data.get("email"),
            "is_admin": data.get("is_admin"),
        }
        check_user_id(conn, id)
        req["id"] = id
        validate_post_users(req)
        update_user(conn, req)
        return jsonify(message=f"product id :{id} successfully updated", status=200)
    elif request.method == "GET":
        user = get_user_by_id(conn, id)
        result = {
            "user_name": user["username"],
            "email": user["email"],
            "is_admin": user["is_admin"],
        }
        return jsonify(message=result, status=200)
    elif request.method == "DELETE":
        delete_user(conn, id)
        return jsonify(message=f"Product id: {id} is deleted successfully", status=200)


@ecommerce.route("/users/<int:id>/cart", methods=["GET", "PUT", "DELETE", "POST"])
def cart(id):
    conn = g.db_connection
    if request.method == "POST":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = {
            "id": id,
            "product_id": data.get("product_id"),
            "quantity": data.get("quantity"),
        }
        check_user_id(conn, id)
        check_product_id(conn, req["product_id"])
        check_product_quantity(conn, (req["product_id"], req["quantity"]))
        insert_cart_products(conn, req)
        return jsonify(message="items added to cart", status=200)
    elif request.method == "PUT":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = {
            "quantity": data.get("quantity"),
            "id": id,
            "product_id": data.get("product_id"),
        }
        check_user_id(conn, id)
        check_product_id(conn, req["product_id"])
        update_cart_products(conn, req)
        return jsonify(message="cart successfully updated", status=200)
    elif request.method == "GET":
        inventories = get_cart_by_user_id(conn, id)
        result = []
        for inventory in inventories:
            result.append(
                {
                    "product_id": inventory["id"],
                    "product_name": inventory["name"],
                    "quantity": inventory["quantity"],
                    "price": inventory["price"],
                }
            )
        return jsonify(message=result, status=200)
    elif request.method == "DELETE":
        req = {
            "id": id,
            "product_id": request.args.get("product_id"),
        }
        delete_cart_item(conn, req)
        return jsonify(message=f"cart item is deleted deleted successfully", status=200)


@ecommerce.route("/users/<int:id>/cart/delete", methods=["DELETE"])
def empty_cart(id):
    conn = g.db_connection
    delete_cart(conn, id)
    return jsonify(message=f"cart items are deleted deleted successfully", status=200)


@ecommerce.route("/users/<int:id>/orders", methods=["GET", "DELETE", "POST"])
def order(id):
    conn = g.db_connection
    if request.method == "POST":
        if not request.is_json:
            return jsonify(message="Data is not in json format", status=400)
        data = request.get_json()
        req = []
        for val in data:
            req.append(
                {"product_id": val.get("product_id"), "quantity": val.get("quantity")}
            )
        check_user_id(conn, id)
        for r in req:
            check_product_id(conn, r["product_id"])
            check_product_quantity(conn, (r["product_id"], r["quantity"]))
        insert_order_products(conn, req, id)
        return jsonify(message="your order is successfull", status=200)
    elif request.method == "GET":
        inventories = get_order_by_user_id(conn, id)
        result = []
        for inventory in inventories:
            result.append(
                {
                    "order_id": inventory["order_id"]
                    "product_id": inventory["product_id"],
                    "product_name": inventory["name"],
                    "quantity": inventory["quantity"],
                    "price": inventory["price"],
                }
            )
        return jsonify(message=result, status=200)
    elif request.method == "DELETE":
        req = {
            "id": id,
            "order_id": request.args.get("order_id"),
        }
        delete_order_item(conn, req)
        return jsonify(
            message=f"Order : {req['order_id']} cancelled successfully", status=200
        )
