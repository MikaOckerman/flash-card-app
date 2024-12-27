from flask import Blueprint, render_template, request, redirect, url_for, redirect, flash, abort
from sqlalchemy.orm import Session
from extensions import db
from models import Flashcard, Category, Tag

flashcards_bp = Blueprint('flashcards', __name__)

@flashcards_bp.route('/study')
def study_mode():
    flashcards = Flashcard.query.all()  # Load all flashcards for now
    return render_template('flashcards/study.html', flashcards=flashcards)

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
        tag_ids = request.form.getlist('tags')
        # Handle "Add New Category"
        if category_id == 'add_new':
            new_category_name = request.form.get('new_category')
        if new_category_name:
            new_category = Category(name=new_category_name)
            db.session.add(new_category)
            db.session.commit()  # Ensure this is committed
            category_id = new_category.id  # Use the new category's ID
            flash('Category added successfully!', 'success')  # Flash success message

        # Handle "Add New Tag(s)"
        if 'add_new' in tag_ids:
            new_tag_name = request.form.get('new_tag')
            if new_tag_name:
                new_tag = Tag(name=new_tag_name)
                db.session.add(new_tag)
                db.session.commit()
                tag_ids.remove('add_new')
                tag_ids.append(new_tag.id)
                flash('New tag added successfully!', 'success')
        new_flashcard = Flashcard(question=question, answer=answer, category_id=category_id)
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                new_flashcard.tags.append(tag)
        db.session.add(new_flashcard)
        db.session.commit()
        flash('Flashcard added successfully!', 'success')
        return redirect(url_for('dashboard'))
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