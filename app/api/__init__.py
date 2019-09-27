from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import discounts, errors  # users, errors, tokens, movies, interactions