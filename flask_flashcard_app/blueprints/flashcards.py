from flask import Blueprint, render_template, request, redirect, url_for, redirect, flash, abort
from markdown import markdown
from sqlalchemy.orm import Session
from extensions import db
from models import Flashcard, Category, Tag

flashcards_bp = Blueprint('flashcards', __name__)

@flashcards_bp.route('/study')
def study_mode():
    flashcards = Flashcard.query.all()
    # Parse Markdown for each flashcard's question and answer
    for flashcard in flashcards:
        flashcard.question = markdown(flashcard.question)
        flashcard.answer = markdown(flashcard.answer)
    return render_template('flashcards/study.html', flashcards=flashcards)

@flashcards_bp.route('/')
def list_flashcards():
    flashcards = Flashcard.query.all()
    # Parse Markdown for each flashcard's question and answer
    for flashcard in flashcards:
        flashcard.question = markdown(flashcard.question)
        flashcard.answer = markdown(flashcard.answer)
    return render_template('flashcards/list.html', flashcards=flashcards)

@flashcards_bp.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        # Get flashcard question and answer
        question = request.form.get('question')
        answer = request.form.get('answer')

        # Handle category
        category_id = request.form.get('category')
        category = Category.query.get(category_id) if category_id else None

        # Handle tags
        tag_ids = request.form.getlist('tags')
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []

        # Create the flashcard
        if question and answer:
            flashcard = Flashcard(
                question=question,
                answer=answer,
                category=category,
                tags=tags
            )
            db.session.add(flashcard)
            db.session.commit()

            flash('Flashcard added successfully!', 'success')
            return redirect(url_for('flashcards.add_flashcard'))
        else:
            flash('Question and answer are required.', 'error')

    # GET method: Render the add flashcard form
    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('flashcards/add.html', categories=categories, tags=tags)

# Edit an existing flashcard
@flashcards_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_flashcard(id):
    flashcard = db.session.get(Flashcard, id)
    if not flashcard:
        abort(404)
    if request.method == 'POST':
        flashcard.question = request.form['question']
        flashcard.answer = request.form['answer']
        category_id = request.form.get('category')
        flashcard.category = Category.query.get(category_id) if category_id else None

        tag_ids = request.form.getlist('tags')
        flashcard.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []

        db.session.commit()
        flash('Flashcard updated successfully!', 'success')
        return redirect(url_for('flashcards.edit'))

    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template(
        'flashcards/edit.html',
        flashcard=flashcard,
        categories=categories,
        tags=tags
    )

# Delete a flashcard
@flashcards_bp.route('/delete/<int:id>', methods=['POST'])
def delete_flashcard(id):
    flashcard = Flashcard.query.get_or_404(id)
    db.session.delete(flashcard)
    db.session.commit()
    flash("Flashcard deleted successfully!", "success")
    return redirect(url_for('flashcards.list_flashcards'))