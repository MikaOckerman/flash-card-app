from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Category

categories_bp = Blueprint('categories', __name__)

# Route to list all categories
@categories_bp.route('/')
def list_categories():
    categories = Category.query.all()
    return render_template('categories/list.html', categories=categories)

# Route to add a new category
@categories_bp.route('/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        if name:  # Simple validation
            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('categories.list_categories'))
    return render_template('categories/add.html')
