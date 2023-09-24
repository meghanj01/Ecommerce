import base64


def encrypt_password(password):
    return base64.b64encode(password.encode("ascii"))
