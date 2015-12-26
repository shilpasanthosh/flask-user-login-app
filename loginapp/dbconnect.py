
from pymongo import MongoClient
# collection = MongoClient()["blog"]["users"]
def connection():
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'Put your secret key here'
    DB_NAME = 'blog'

    DATABASE = MongoClient()[DB_NAME]
    POSTS_COLLECTION = DATABASE.posts
    USERS_COLLECTION = DATABASE.users
    SETTINGS_COLLECTION = DATABASE.settings
    collection = MongoClient()["blog"]["users"]

    DEBUG = True
    return collection




