from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import cv2
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'image-enhancement-secret-key'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, 'static', 'input')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'static', 'output')

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(BASE_DIR, 'image.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}


# ---------------- DATABASE MODELS ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ImageRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    enhanced_filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


# ---------------- LOGIN PROTECTION ----------------

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view


# ---------------- IMAGE VALIDATION ----------------

def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ---------------- MAIN PAGE ----------------

@app.route('/', methods=['GET', 'POST'])
def index():
    original = None
    enhanced = None

    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please log in before enhancing an image.')
            return redirect(url_for('login'))

        image = request.files.get('image')

        if not image or image.filename == '':
            flash('Please select an image.')
            return redirect(url_for('index'))

        if not allowed_file(image.filename):
            flash('Please upload a valid image file.')
            return redirect(url_for('index'))

        filename = secure_filename(image.filename)

        if not filename or '.' not in filename:
            flash('Invalid filename.')
            return redirect(url_for('index'))

        unique_name = datetime.now().strftime('%Y%m%d%H%M%S%f')
        extension = filename.rsplit('.', 1)[1].lower()

        original_filename = f'{unique_name}.{extension}'
        enhanced_filename = f'enhanced_{unique_name}.{extension}'

        input_path = os.path.join(INPUT_FOLDER, original_filename)
        output_path = os.path.join(OUTPUT_FOLDER, enhanced_filename)

        try:
            image.save(input_path)
            img = cv2.imread(input_path)

            if img is None:
                os.remove(input_path)
                flash('Could not read the image. Try another image.')
                return redirect(url_for('index'))

            enhanced_img = cv2.detailEnhance(
                img, sigma_s=10, sigma_r=0.15
            )

            if not cv2.imwrite(output_path, enhanced_img):
                os.remove(input_path)
                flash('Could not save the enhanced image.')
                return redirect(url_for('index'))

            record = ImageRecord(
                original_filename=original_filename,
                enhanced_filename=enhanced_filename
            )

            db.session.add(record)
            db.session.commit()

            original = original_filename
            enhanced = enhanced_filename
            flash('Image enhanced successfully!')

        except Exception:
            db.session.rollback()
            app.logger.exception('Image processing failed')

            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)

            flash('An error occurred while processing the image.')

    records = ImageRecord.query.order_by(
        ImageRecord.upload_time.desc()
    ).all()

    return render_template(
        'index.html',
        original=original,
        enhanced=enhanced,
        records=records,
        username=session.get('username')
    )


# ---------------- DASHBOARD ----------------

@app.route('/home')
@login_required
def home():
    return redirect(url_for('index'))


# ---------------- SIGNUP ----------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('Please fill in all fields.')
            return redirect(url_for('signup'))

        if len(password) < 8:
            flash('Password must be at least 8 characters long.')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('This email is already registered. Please log in.')
            return redirect(url_for('login'))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))

        except Exception:
            db.session.rollback()
            app.logger.exception('Signup failed')
            flash('Could not create your account. Please try again.')
            return redirect(url_for('signup'))

    return render_template('signup.html')


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True

            flash('Login successful!')
            return redirect(url_for('index'))

        flash('Invalid email or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# ---------------- ABOUT & HELP ----------------

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')


# ---------------- UPLOAD PAGE ----------------

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('upload.html')


# ---------------- RUN APP ----------------

if __name__ == '__main__':
    app.run(debug=True)
