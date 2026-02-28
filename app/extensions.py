"""
Flask extensions initialization.
Centralizes all extension instances so they can be imported anywhere.
"""
from flask_jwt_extended import JWTManager

jwt = JWTManager()
