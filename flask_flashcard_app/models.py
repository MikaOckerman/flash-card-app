from extensions import db

# Flashcard Model
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tags = db.relationship('Tag', secondary='flashcard_tag', back_populates='flashcards')
    times_studied = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.DateTime)

# Category Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    flashcards = db.relationship('Flashcard', backref='category', lazy=True)

# Tag Model
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Many-to-Many relationship with flashcards
    flashcards = db.relationship('Flashcard', secondary='flashcard_tag', back_populates='tags')


# Flashcard-Tag Many-to-Many Table
flashcard_tag = db.Table(
    'flashcard_tag',
    db.Column('flashcard_id', db.Integer, db.ForeignKey('flashcard.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
