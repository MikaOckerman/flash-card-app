from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
    name = request.json.get('name') if request.is_json else request.form.get('name')

    if not name:
        return jsonify({'error': 'Category name is required'}), 400

    # Check for duplicates
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({'error': 'Category already exists'}), 400

    # Add new category
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    # Return all categories (for dropdown reload)
    all_categories = Category.query.all()
    categories_list = [{'id': category.id, 'name': category.name} for category in all_categories]
    return jsonify(categories_list), 201
