from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == 'POST':
        name = request.form['name']
        if name:  # Simple validation
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for('tags.list_tags'))
    return render_template('tags/add.html')
