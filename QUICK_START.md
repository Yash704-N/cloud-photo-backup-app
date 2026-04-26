# Cloud Photo Backup App - Quick Start Guide

## ⚡ Quick Start (2 Minutes)

### For Windows:
```bash
# 1. Navigate to project folder
cd cloud-photo-backup

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py

# 6. Open browser to http://localhost:5000
```

### For Mac/Linux:
```bash
cd cloud-photo-backup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application (all routes and logic) |
| `requirements.txt` | Python dependencies to install |
| `static/style.css` | All styling and responsive design |
| `static/script.js` | JavaScript utilities and interactions |
| `templates/base.html` | Base template with navbar/footer |
| `templates/login.html` | User login page |
| `templates/register.html` | User registration page |
| `templates/dashboard.html` | User dashboard with stats |
| `templates/gallery.html` | Photo gallery view |
| `templates/upload.html` | Photo upload interface |
| `templates/404.html` | 404 error page |
| `templates/500.html` | 500 error page |
| `uploads/` | Stores user photos (auto-created) |
| `database.db` | SQLite database (auto-created) |

---

## 🔑 Key Features

✅ User Registration & Secure Login  
✅ Upload Photos (JPG, PNG, JPEG - max 10MB)  
✅ View in Beautiful Gallery  
✅ Download & Delete Photos  
✅ Search by Filename  
✅ Dashboard with Statistics  
✅ Dark Mode Support  
✅ Fully Responsive Design  

---

## 📝 Test Account

Create your own during registration!

---

## 🔒 Security Features

- Passwords hashed with Werkzeug
- File type validation
- File size validation  
- User-specific file storage
- Session-based authentication
- SQL injection prevention

---

## 🎨 Design Highlights

- Modern cloud-themed interface
- Responsive on all devices (mobile, tablet, desktop)
- Smooth animations and transitions
- Toast notifications for feedback
- Confirmation modals for destructive actions
- Loading indicators for uploads
- Dark mode toggle

---

## 📊 Database Structure

**Users Table**: Stores username, email, hashed password  
**Photos Table**: Stores photo metadata, linked to users

---

## 🚀 Routes

- `/` - Home (redirects based on login status)
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/dashboard` - User dashboard
- `/gallery` - Photo gallery
- `/upload` - Upload photos
- `/download/<filename>` - Download photo
- `/delete/<filename>` - Delete photo

---

## 🐛 Troubleshooting

**Port already in use?**  
Change port in app.py line ~520

**Python not found?**  
Use full path: `C:\Python39\python.exe app.py`

**Module not found?**  
Ensure virtual environment is activated

**Database error?**  
Delete database.db and restart app

---

## 📖 Documentation

All documentation is in the project folder:
- `README.md` - Full project overview
- `INSTALLATION_GUIDE.md` - Detailed setup
- `PROJECT_ABSTRACT.md` - Project summary
- `PROBLEM_STATEMENT.md` - Problem definition
- `OBJECTIVES.md` - Project goals
- `MODULES_EXPLANATION.md` - Technical details
- `FUTURE_SCOPE.md` - Future enhancements
- `VIVA_QUESTIONS.md` - Interview prep (55 Q&A)
- `PPT_CONTENT.md` - Presentation content

---

## 💡 Tips

- App uses Flask development server (not for production)
- Database creates automatically on first run
- Photos stored in user-specific folders
- Modify secret_key in app.py for production
- Check console for error messages

---

## 🎓 Educational Value

Perfect for learning:
- Flask web framework
- SQLite database design
- HTML/CSS responsive design
- JavaScript interactions
- Security best practices
- File upload handling
- User authentication

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2026
