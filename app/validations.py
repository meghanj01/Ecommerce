import re
from flask import abort, make_response, jsonify
from .config import PRODUCT_NAME, USER_NAME, EMAIL, PASSWORD, TRUE, FLASE


def validate_post_products(data):
    if not data["product_name"] or not re.fullmatch(PRODUCT_NAME, data["product_name"]):
        abort(make_response(jsonify(message="Invalid product name", status=400)))

    if not data["product_quantity"] or data["product_quantity"] > 1000:
        abort(make_response(jsonify(message="Invalid product quantity", status=400)))

    if not data["price"] or 0.01 > data["price"] > 99999999.99:
        abort(make_response(jsonify(message="Invalid price", status=400)))
    return


def validate_post_users(data):
    if not data["user_name"] or not re.fullmatch(USER_NAME, data["user_name"]):
        abort(make_response(jsonify(message="Invalid user name", status=400)))

    if not data["password"] or not re.fullmatch(PASSWORD, data["password"]):
        abort(make_response(jsonify(message="Invalid password", status=400)))

    if not data["email"] or not re.fullmatch(EMAIL, data["email"]):
        abort(make_response(jsonify(message="Invalid email", status=400)))
    if data["is_admin"] is None or not data["is_admin"] in [TRUE, FLASE]:
        abort(make_response(jsonify(message="Invalid is_admin", status=400)))
    return


# def validate_put_products(data):

#     if  data["product_name"] :
#         if not re.fullmatch(
#         "[A-Za-z]{2,25}( [A-Za-z]{2,25})?", data["product_name"]):
#             abort(make_response(jsonify(message="Invalid product name", status=400)))

#     if not data["product_quantity"] or data["product_quantity"] > 1000:
#         abort(make_response(jsonify(message="Invalid product quantity", status=400)))

#     if not data["price"] or 0.01 > data["price"] > 99999999.99:
#         abort(make_response(jsonify(message="Invalid price", status=400)))
#     return
