from flask import Flask, g, jsonify
from utils.logger import logger
from app import route
from app.db import initialize_connection

app = Flask(__name__)
app.register_blueprint(route.ecommerce)

connection = initialize_connection()


@app.route("/")
def check_health():
    return jsonify(message="Running", status=200)


@app.before_request
def before_request():
    logger.debug("started executing")
    g.db_connection = connection.get_connection()
    print("Started executing ")


@app.after_request
def after_request(response):
    logger.debug("Exicting request")
    print("exicting request")
    if hasattr(g, "db_connection"):
        connection.release_connection(g.db_connection)
    return response


if __name__ == "__main__":
    app.run(debug=True)
