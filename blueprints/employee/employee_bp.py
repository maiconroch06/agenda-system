from flask import Blueprint, render_template, redirect, url_for

employee_bp = Blueprint('employee', __name__, template_folder='templates')