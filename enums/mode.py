from .meta_enum import BaseEnum


class Mode(str, BaseEnum):
    text = 'text'
    json = 'json'
    env = 'env'
    integrate = 'integrate'
