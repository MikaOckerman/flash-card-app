from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from extensions import db
from models import Tag

tags_bp = Blueprint('tags', __name__)

# Route to list all tags
@tags_bp.route('/')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

# Route to add a new tag
@tags_bp.route('/add', methods=['GET', 'POST'])
def add_tag():
    name = request.json.get('name') if request.is_json else request.form.get('name')

    if not name:
        return jsonify({'error': 'Tag name is required'}), 400

    # Check for duplicates
    existing_tag = Tag.query.filter_by(name=name).first()
    if existing_tag:
        return jsonify({'error': 'Tag already exists'}), 400

    # Add new tag
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    # Return all tags (for dropdown reload)
    all_tags = Tag.query.all()
    tags_list = [{'id': tag.id, 'name': tag.name} for tag in all_tags]
    return jsonify(tags_list), 201
