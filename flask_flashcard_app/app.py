from flask import Flask, render_template
from extensions import db
from flask_migrate import Migrate
from blueprints.flashcards import flashcards_bp
from blueprints.categories import categories_bp
from blueprints.tags import tags_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mika:1234@localhost:5432/flashcard_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fast_flash_frenzy_!88'


db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(flashcards_bp, url_prefix='/flashcards')
app.register_blueprint(categories_bp, url_prefix='/categories')
app.register_blueprint(tags_bp, url_prefix='/tags')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/test_db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"
