# Cloud Photo Backup App - Installation Guide

## Prerequisites

Before installing the Cloud Photo Backup App, ensure you have the following installed on your system:

- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **pip** (Python Package Manager) - Usually comes with Python
- **Git** (Optional) - For version control

---

## Installation Steps

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd cloud-photo-backup

# OR manually download and extract the ZIP file
# Navigate to the extracted folder
cd cloud-photo-backup
```

### Step 2: Create Virtual Environment

Creating a virtual environment is recommended to isolate project dependencies.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask: Web framework for Python
- Werkzeug: WSGI utilities for secure password hashing

### Step 4: Initialize the Database

The database will be automatically created on first run. If you want to manually initialize:

```bash
python
>>> from app import init_db
>>> init_db()
>>> exit()
```

### Step 5: Run the Application

```bash
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 6: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

---

## Usage

### Creating an Account

1. Click on **"Register here"** link on the login page
2. Enter your details:
   - **Username**: Minimum 3 characters
   - **Email**: Valid email address
   - **Password**: Minimum 6 characters
3. Click **Create Account**

### Login

1. Enter your username and password
2. Click **Login**

### Uploading Photos

1. Go to **Upload** page
2. Either:
   - Drag and drop photos
   - Click "Choose Files" to browse
3. Photos must be JPG, JPEG, or PNG (max 10MB)
4. Wait for upload to complete

### Viewing Gallery

1. Go to **Gallery** page
2. View all your uploaded photos in a grid layout
3. Use search to find photos by filename

### Downloading Photos

1. Go to **Gallery**
2. Hover over a photo
3. Click the download icon to download original photo

### Deleting Photos

1. Go to **Gallery**
2. Hover over a photo
3. Click the trash icon to delete
4. Confirm deletion in the modal

### Dark Mode

- Click the moon/sun icon in the top right navigation
- Your preference is saved automatically

---

## Project Structure

```
cloud-photo-backup/
├── app.py                 # Main Flask application
├── database.db           # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
│
├── static/
│   ├── style.css        # Main stylesheet
│   └── script.js        # JavaScript utilities
│
├── templates/
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # Dashboard
│   ├── gallery.html     # Photo gallery
│   ├── upload.html      # Upload page
│   ├── 404.html         # Error page
│   └── 500.html         # Error page
│
└── uploads/             # User photo storage
    └── user_1/          # User-specific folders
    └── user_2/
```

---

## Configuration

### Change Secret Key (Important for Production)

In `app.py`, line 20:

```python
# Before:
app.secret_key = 'your-secret-key-change-in-production'

# After (use a strong random key):
app.secret_key = 'your-generated-strong-secret-key-here'
```

Generate a strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### Modify Port

In `app.py`, line ~520:

```python
app.run(debug=True, host='localhost', port=5000)
```

Change `port=5000` to your desired port number.

---

## Troubleshooting

### Issue: "Python not found"
- **Solution**: Add Python to system PATH or use full path to python executable

### Issue: "Module not found: Flask"
- **Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Issue: "Port 5000 is already in use"
- **Solution**: Change port in app.py or kill process using the port

### Issue: "Database locked"
- **Solution**: Close any other instances of the app and delete `database.db` to reset

### Issue: "File upload not working"
- **Solution**: Ensure `uploads` folder exists and has write permissions

---

## Database Management

### View Database Contents

```python
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# View all users
c.execute('SELECT * FROM users')
print(c.fetchall())

# View all photos
c.execute('SELECT * FROM photos')
print(c.fetchall())

conn.close()
```

### Reset Database

```bash
# Delete the database file
rm database.db  # On macOS/Linux
del database.db # On Windows

# Restart the app to create a fresh database
python app.py
```

---

## Deployment to Production

### Security Checklist

- [ ] Change `debug=False`
- [ ] Generate and use a strong `secret_key`
- [ ] Use HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Validate and sanitize all inputs
- [ ] Use environment variables for sensitive data
- [ ] Set up proper logging
- [ ] Regular database backups

### Deployment Options

1. **Heroku**
2. **PythonAnywhere**
3. **AWS**
4. **Azure**
5. **DigitalOcean**
6. **Render.com**

---

## Development Tips

### Enable Debug Mode

Already enabled by default in development.

### Clear Browser Cache

```javascript
// In browser console
localStorage.clear()
sessionStorage.clear()
```

### View Application Logs

Logs are printed to console by default.

---

## Support and Issues

If you encounter any issues:

1. Check the error message in the console
2. Review the troubleshooting section above
3. Check that all files are in the correct directories
4. Verify Python version compatibility
5. Ensure all dependencies are installed

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Documentation](https://docs.python.org/3/)
- [Werkzeug Documentation](https://werkzeug.palletsprojects.com/)

---

## License

This project is created for educational purposes as a mini project for final-year students.

---

## Version

**Version**: 1.0.0  
**Last Updated**: 2026  
**Status**: Stable
