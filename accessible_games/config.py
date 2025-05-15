import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///games.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
