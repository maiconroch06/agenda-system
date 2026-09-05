import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request, session

from models import User
from models import Address

user_login = Blueprint('login', __name__, template_folder='templates')

@user_login.route('/', methods=['GET'])
def login():
    return render_template('/login.html')