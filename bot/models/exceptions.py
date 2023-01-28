class ModelException(Exception):
    """Custom exceptions when interacting with models"""


class CurrencyException(ModelException):
    """Error when working with the Currency model"""


class UserException(ModelException):
    """Error when working with the User model"""
