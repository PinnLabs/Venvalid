from datetime import datetime
from decimal import Decimal
from pathlib import Path


def str_(default=None, allowed=None, validate=None):
    return (str, {"default": default, "allowed": allowed, "validate": validate})


def int_(default=None, allowed=None, validate=None):
    return (int, {"default": default, "allowed": allowed, "validate": validate})


def bool_(default=None):
    return (bool, {"default": default})


def list_(default=None):
    return (list, {"default": default})


def path_(default=None):
    return (Path, {"default": default})


def decimal_(default=None):
    return (Decimal, {"default": default})


def datetime_(default=None):
    return (datetime, {"default": default})


def json_(default=None):
    return (dict, {"default": default})
