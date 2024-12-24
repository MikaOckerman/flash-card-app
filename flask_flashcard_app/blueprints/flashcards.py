from flask import Blueprint, render_template, request, redirect, url_for, redirect, flash, abort
from sqlalchemy.orm import Session
from extensions import db
from models import Flashcard, Category, Tag

flashcards_bp = Blueprint('flashcards', __name__)

@flashcards_bp.route('/')
def list_flashcards():
    flashcards = Flashcard.query.all()
    return render_template('flashcards/list.html', flashcards=flashcards)

@flashcards_bp.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category_id = request.form['category']
        new_flashcard = Flashcard(question=question, answer=answer, category_id=category_id)
        db.session.add(new_flashcard)
        db.session.commit()
        return redirect(url_for('flashcards.list_flashcards'))
    categories = Category.query.all()
    return render_template('flashcards/add.html', categories=categories)

# Edit an existing flashcard
@flashcards_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_flashcard(id):
    flashcard = db.session.get(Flashcard, id)
    if not flashcard:
        abort(404)
    if request.method == 'POST':
        flashcard.question = request.form['question']
        flashcard.answer = request.form['answer']
        flashcard.category_id = request.form['category']
        db.session.commit()
        flash("Flashcard updated successfully!", "success")
        return redirect(url_for('flashcards.list_flashcards'))
    categories = Category.query.all()
    return render_template('flashcards/edit.html', flashcard=flashcard, categories=categories)

# Delete a flashcard
@flashcards_bp.route('/delete/<int:id>', methods=['POST'])
def delete_flashcard(id):
    flashcard = Flashcard.query.get_or_404(id)
    db.session.delete(flashcard)
    db.session.commit()
    flash("Flashcard deleted successfully!", "success")
    return redirect(url_for('flashcards.list_flashcards'))