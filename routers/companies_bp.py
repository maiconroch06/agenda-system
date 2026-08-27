from flask import Blueprint, render_template, redirect, url_for

companies_bp = Blueprint('companies', __name__, template_folder='templates')