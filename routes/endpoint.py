from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

endpoint = Blueprint('pages', __name__)

@endpoint.route('/')
def homepage():
    return render_template("home.html")