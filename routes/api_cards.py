from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

api_cards_bp = Blueprint('api_cards', __name__)


@api_cards_bp.route('/', methods=["POST"]) # to make new card
def post_card():
    pass

@api_cards_bp.route('/<int:card_id>', methods=["PUT"]) # to update a card (using card_id)
def put_card(card_id):
    pass

@api_cards_bp.route('/<int:card_id>', methods=["POST"]) # to delete a card (using HTML)
def delete_card(card_id):
    pass