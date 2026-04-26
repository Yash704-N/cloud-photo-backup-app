"""
Cloud Photo Backup App
A SaaS-based web application for storing, managing, and sharing personal photos
Author: Student Name
Date: 2026
"""

from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
from functools import wraps
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


# ==================== DATABASE FUNCTIONS ====================

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create photos table
    c.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_size INTEGER,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()


# ==================== AUTHENTICATION ====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_user_upload_folder(user_id):
    """Get user-specific upload folder"""
    user_folder = os.path.join(UPLOAD_FOLDER, f'user_{user_id}')
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else to login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        error = None
        
        if not username or len(username) < 3:
            error = 'Username must be at least 3 characters long'
        elif not email or '@' not in email:
            error = 'Invalid email address'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters long'
        elif password != confirm_password:
            error = 'Passwords do not match'
        
        if error is None:
            conn = get_db_connection()
            c = conn.cursor()
            
            try:
                hashed_password = generate_password_hash(password)
                c.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, hashed_password)
                )
                conn.commit()
                conn.close()
                
                return redirect(url_for('login', success='Registration successful! Please login.'))
            
            except sqlite3.IntegrityError:
                error = 'Username or email already exists'
                conn.close()
        
        return render_template('register.html', error=error)
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        error = None
        
        if not username or not password:
            error = 'Username and password are required'
        
        if error is None:
            conn = get_db_connection()
            c = conn.cursor()
            
            user = c.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            conn.close()
            
            if user is None:
                error = 'Incorrect username'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password'
            
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
        
        return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route - shows user statistics"""
    user_id = session['user_id']
    username = session['username']
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get total photos count
    total_photos = c.execute(
        'SELECT COUNT(*) as count FROM photos WHERE user_id = ?',
        (user_id,)
    ).fetchone()['count']
    
    # Get total storage used
    storage_used = c.execute(
        'SELECT SUM(file_size) as total FROM photos WHERE user_id = ?',
        (user_id,)
    ).fetchone()['total'] or 0
    
    # Get recent photos
    recent_photos = c.execute(
        'SELECT * FROM photos WHERE user_id = ? ORDER BY upload_date DESC LIMIT 6',
        (user_id,)
    ).fetchall()
    
    conn.close()
    
    storage_mb = round(storage_used / (1024 * 1024), 2)
    
    return render_template(
        'dashboard.html',
        username=username,
        total_photos=total_photos,
        storage_used=storage_mb,
        recent_photos=recent_photos
    )


@app.route('/gallery')
@login_required
def gallery():
    """Gallery page - shows all user photos"""
    user_id = session['user_id']
    search = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    c = conn.cursor()
    
    if search:
        photos = c.execute(
            'SELECT * FROM photos WHERE user_id = ? AND original_filename LIKE ? ORDER BY upload_date DESC',
            (user_id, f'%{search}%')
        ).fetchall()
    else:
        photos = c.execute(
            'SELECT * FROM photos WHERE user_id = ? ORDER BY upload_date DESC',
            (user_id,)
        ).fetchall()
    
    conn.close()
    
    return render_template('gallery.html', photos=photos, search=search)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload photo route"""
    if request.method == 'POST':
        user_id = session['user_id']
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Only JPG, JPEG, PNG files allowed'}), 400
        
        # Get file size - more efficient way
        file_size = len(file.read())
        file.seek(0)  # Reset to beginning for save
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'message': 'File size exceeds 10MB limit'}), 400
        
        if file_size == 0:
            return jsonify({'success': False, 'message': 'Cannot upload empty file'}), 400
        
        # Create user folder and save file
        user_folder = get_user_upload_folder(user_id)
        secure_name = secure_filename(file.filename)
        
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + secure_name
        
        filepath = os.path.join(user_folder, filename)
        
        # Save file and database in optimized way
        try:
            file.save(filepath)
            
            # Save metadata to database
            conn = get_db_connection()
            c = conn.cursor()
            
            c.execute(
                'INSERT INTO photos (user_id, filename, original_filename, file_size) VALUES (?, ?, ?, ?)',
                (user_id, filename, secure_name, file_size)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            return jsonify({'success': False, 'message': f'Upload failed: {str(e)}'}), 500
        
        return jsonify({'success': True, 'message': 'Photo uploaded successfully'})
    
    return render_template('upload.html')


@app.route('/download/<filename>')
@login_required
def download(filename):
    """Download photo route"""
    user_id = session['user_id']
    
    # Verify that the file belongs to the user
    conn = get_db_connection()
    c = conn.cursor()
    
    photo = c.execute(
        'SELECT * FROM photos WHERE user_id = ? AND filename = ?',
        (user_id, filename)
    ).fetchone()
    conn.close()
    
    if photo is None:
        return 'File not found or you do not have permission to download', 404
    
    user_folder = get_user_upload_folder(user_id)
    filepath = os.path.join(user_folder, filename)
    
    if not os.path.exists(filepath):
        return 'File not found', 404
    
    return send_file(
        filepath,
        as_attachment=True,
        download_name=photo['original_filename']
    )


@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete(filename):
    """Delete photo route"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Verify ownership
    photo = c.execute(
        'SELECT * FROM photos WHERE user_id = ? AND filename = ?',
        (user_id, filename)
    ).fetchone()
    
    if photo is None:
        conn.close()
        return jsonify({'success': False, 'message': 'File not found or permission denied'}), 403
    
    # Delete from database
    c.execute('DELETE FROM photos WHERE id = ?', (photo['id'],))
    conn.commit()
    conn.close()
    
    # Delete physical file
    user_folder = get_user_upload_folder(user_id)
    filepath = os.path.join(user_folder, filename)
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        app.logger.error(f"Error deleting file: {str(e)}")
    
    return jsonify({'success': True, 'message': 'Photo deleted successfully'})


@app.route('/search')
@login_required
def search_api():
    """API endpoint for search"""
    user_id = session['user_id']
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    conn = get_db_connection()
    c = conn.cursor()
    
    results = c.execute(
        'SELECT * FROM photos WHERE user_id = ? AND original_filename LIKE ? ORDER BY upload_date DESC',
        (user_id, f'%{query}%')
    ).fetchall()
    conn.close()
    
    return jsonify([dict(photo) for photo in results])


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run Flask app in development mode
    app.run(debug=True, host='localhost', port=5000)
