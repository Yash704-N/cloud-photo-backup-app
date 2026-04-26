# Cloud Photo Backup App - Modules Explanation

## Overview

The Cloud Photo Backup App is built using a modular architecture consisting of Backend (Flask), Frontend (HTML/CSS/JavaScript), and Database (SQLite) layers. This document explains each module in detail.

---

## Module Structure

```
Cloud Photo Backup App
├── Backend Module (app.py)
├── Database Module (SQLite)
├── Frontend Module
│   ├── Templates (HTML)
│   ├── Styling (CSS)
│   └── Interactivity (JavaScript)
└── Static Assets
```

---

## 1. Backend Module (app.py)

### 1.1 Overview
The backend module is the core of the application, handling all server-side operations using Flask.

### 1.2 Module Components

#### A. Configuration & Initialization

```python
# Flask app initialization
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

**Purpose**: Sets up Flask application, configuration variables, and security settings.

**Key Functions**:
- `init_app()`: Initialize Flask app
- `set_config()`: Configure application parameters

#### B. Database Layer

```python
def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    # Creates users and photos tables
```

**Purpose**: Manages database connectivity and initialization.

**Key Functions**:
- `get_db_connection()`: Returns database connection
- `init_db()`: Creates database schema on startup

#### C. Authentication Module

```python
def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    # Validates input
    # Hashes password with Werkzeug
    # Stores user in database

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    # Validates credentials
    # Creates session
    # Redirects to dashboard

@app.route('/logout')
def logout():
    """User logout route"""
    # Clears session
    # Redirects to login
```

**Purpose**: Handles user authentication and authorization.

**Key Functions**:
- `login_required()`: Decorator for protected routes
- `register()`: User registration
- `login()`: User authentication
- `logout()`: Session termination

#### D. File Upload Module

```python
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_upload_folder(user_id):
    """Get user-specific upload folder"""
    user_folder = os.path.join(UPLOAD_FOLDER, f'user_{user_id}')
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload photo route"""
    # Validates file type
    # Checks file size
    # Generates unique filename
    # Saves to user folder
    # Stores metadata in database
```

**Purpose**: Manages photo uploads with validation and storage.

**Key Functions**:
- `allowed_file()`: Validates file extensions
- `get_user_upload_folder()`: Creates user storage directory
- `upload()`: Handles file upload

#### E. Gallery Module

```python
@app.route('/gallery')
@login_required
def gallery():
    """Gallery page - shows all user photos"""
    # Retrieves user's photos
    # Handles search filter
    # Returns paginated results

@app.route('/search')
@login_required
def search_api():
    """API endpoint for search"""
    # Searches photos by filename
    # Returns JSON results
```

**Purpose**: Displays and manages photo gallery with search.

**Key Functions**:
- `gallery()`: Main gallery page
- `search_api()`: Search API endpoint

#### F. Dashboard Module

```python
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route - shows user statistics"""
    # Calculates total photos
    # Calculates storage used
    # Gets recent uploads
    # Renders dashboard
```

**Purpose**: Displays user dashboard with statistics.

**Key Functions**:
- `dashboard()`: Renders dashboard with stats

#### G. Download/Delete Module

```python
@app.route('/download/<filename>')
@login_required
def download(filename):
    """Download photo route"""
    # Verifies user ownership
    # Retrieves file
    # Sends to client

@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete(filename):
    """Delete photo route"""
    # Verifies ownership
    # Deletes from database
    # Deletes file from storage
```

**Purpose**: Manages photo downloads and deletion.

**Key Functions**:
- `download()`: File download handler
- `delete()`: Photo deletion handler

#### H. Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500
```

**Purpose**: Handles HTTP errors gracefully.

### 1.3 Request Flow

```
Request → Route Handler → Validation → Database Operation → Response
```

---

## 2. Database Module (SQLite)

### 2.1 Overview
SQLite database stores all application data with two main tables.

### 2.2 Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns**:
- `id`: Unique user identifier (auto-increment)
- `username`: Unique username (required)
- `email`: Unique email address (required)
- `password`: Hashed password (required)
- `created_at`: Account creation timestamp

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE on `username` and `email`

### 2.3 Photos Table

```sql
CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Columns**:
- `id`: Unique photo identifier (auto-increment)
- `user_id`: References user (FK)
- `filename`: Stored filename with timestamp
- `original_filename`: Original filename
- `file_size`: File size in bytes
- `upload_date`: Upload timestamp

**Constraints**:
- FOREIGN KEY: Maintains referential integrity
- ON DELETE CASCADE: Deletes photos when user deleted

### 2.4 Query Examples

```python
# Insert user
INSERT INTO users (username, email, password) 
VALUES (?, ?, ?)

# Retrieve user
SELECT * FROM users WHERE username = ?

# Insert photo
INSERT INTO photos (user_id, filename, original_filename, file_size)
VALUES (?, ?, ?, ?)

# Get user photos
SELECT * FROM photos WHERE user_id = ? ORDER BY upload_date DESC

# Search photos
SELECT * FROM photos WHERE user_id = ? AND original_filename LIKE ?

# Delete photo
DELETE FROM photos WHERE id = ?
```

---

## 3. Frontend Module

### 3.1 HTML Templates

#### A. base.html
**Purpose**: Base template for all pages.

**Components**:
- Navigation bar with logo and menu
- User info (username, logout button)
- Dark mode toggle
- Footer
- Main content block
- Font Awesome icons
- Responsive meta tags

**Key Sections**:
```html
- Head (meta, CSS, icons)
- Navbar (navigation, user menu)
- Main content (block for child templates)
- Footer (copyright, info)
- Scripts (JS files)
```

#### B. login.html
**Purpose**: User login page.

**Features**:
- Username input field
- Password input field
- Login button
- Error display
- Registration link
- Success message display
- Background shapes (CSS animations)
- Features list

**Form Fields**:
- username (required)
- password (required)

#### C. register.html
**Purpose**: User registration page.

**Features**:
- Username input (min 3 chars)
- Email input (validation)
- Password input (min 6 chars)
- Confirm password field
- Form validation messages
- Login link
- Background animations

**Form Fields**:
- username (min 3 characters)
- email (valid format)
- password (min 6 characters)
- confirm_password (match verification)

#### D. dashboard.html
**Purpose**: User dashboard with statistics.

**Sections**:
- Welcome message with username
- Statistics cards (total photos, storage, status)
- Quick action buttons (Upload, Gallery, Logout)
- Recent photos grid (up to 6)
- Features information section
- Empty state when no photos

**Data Displayed**:
- Total photos count
- Storage used (MB)
- Cloud status
- Recent uploads
- Features list

#### E. gallery.html
**Purpose**: Photo gallery with search and management.

**Features**:
- Gallery header with photo count
- Search bar with icon
- Responsive photo grid
- Photo overlay with actions
- Download and delete buttons
- Delete confirmation modal
- Empty state
- Lazy loading for images

**Components**:
- Search functionality
- Photo grid (responsive)
- Photo overlay (on hover)
- Delete modal
- Notifications

#### F. upload.html
**Purpose**: Photo upload interface.

**Features**:
- Drag and drop zone
- File browser button
- File requirements list
- Upload progress display
- Upload summary
- Tips section
- Multiple file support
- Real-time progress tracking

**Upload Process**:
1. Select/drag files
2. Validate files
3. Show progress
4. Display results
5. Offer next steps

#### G. 404.html & 500.html
**Purpose**: Error pages.

**Features**:
- Error icon
- Error code (404/500)
- Error message
- Link to home

### 3.2 CSS Module (style.css)

#### A. CSS Structure

```css
:root {
    /* CSS Variables */
    --primary-color: #0066ff
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1)
    /* More variables... */
}
```

#### B. Main Sections

1. **Global Styles**
   - Reset and defaults
   - Typography
   - Color scheme

2. **Layout**
   - Container
   - Main content
   - Responsive grid

3. **Components**
   - Navigation
   - Buttons
   - Forms
   - Cards
   - Modals

4. **Pages**
   - Authentication
   - Dashboard
   - Gallery
   - Upload

5. **Responsive Design**
   - Desktop (1200px+)
   - Tablet (768px-1199px)
   - Mobile (below 768px)

#### C. Key Features

- **CSS Variables**: For easy theming
- **Flexbox & Grid**: Modern layout
- **Animations**: Smooth transitions
- **Dark Mode**: CSS variable switching
- **Responsive**: Mobile-first approach
- **Accessibility**: Proper contrast ratios

### 3.3 JavaScript Module (script.js)

#### A. Dark Mode Toggle

```javascript
function toggleDarkMode() {
    // Toggles dark-mode class on body
    // Saves preference to localStorage
    // Updates icon
}
```

#### B. Form Validation

```javascript
function validateEmail(email) { }
function validatePasswordStrength(password) { }
function validateFileExtension(filename) { }
function validateFileSize(fileSize) { }
```

#### C. Utilities

```javascript
function formatFileSize(bytes) { }
function formatDate(dateString) { }
function debounce(func, delay) { }
function throttle(func, delay) { }
```

#### D. Storage Utilities

```javascript
function saveToLocalStorage(key, value) { }
function getFromLocalStorage(key) { }
function removeFromLocalStorage(key) { }
```

#### E. Upload Handling

```javascript
function handleFiles(files) { }
function uploadFile(file) { }
function showUploadProgress(fileId, percent) { }
function showUploadSummary() { }
```

#### F. Event Handlers

- Keyboard shortcuts (Ctrl+K for search)
- Escape key for modal closing
- Scroll to top button
- Search functionality

---

## 4. Module Interactions

### 4.1 User Registration Flow

```
User Input → Form Validation → POST /register
→ Backend Validation → Password Hash → Store in DB
→ Redirect to Login → Login Page Rendered
```

### 4.2 Photo Upload Flow

```
Drag/Drop Files → File Validation → POST /upload
→ Backend File Validation → Generate Unique Name
→ Save to User Folder → Store Metadata in DB
→ Return Success → Display in Gallery
```

### 4.3 Gallery Display Flow

```
User Click Gallery → GET /gallery → Query DB
→ Retrieve User Photos → Render Template
→ Send HTML to Client → Load Images → Display Gallery
```

### 4.4 Photo Download Flow

```
User Click Download → GET /download/<filename>
→ Verify Ownership → Load File → Send to Browser
→ Save on User Device
```

---

## 5. Data Flow

### 5.1 Request-Response Cycle

```
Client Request
    ↓
Flask Route Handler
    ↓
Input Validation
    ↓
Business Logic
    ↓
Database Query
    ↓
Template Rendering
    ↓
Response to Client
    ↓
Client Processes Response
```

### 5.2 Session Management

```
User Login → Session Created → Stored in Memory
    ↓ (On Each Request)
Session Validated → User Authenticated → Allow Access
    ↓ (On Logout)
Session Cleared → User Logged Out → Redirect to Login
```

---

## 6. Module Dependencies

```
Frontend (HTML/CSS/JS)
    ↓
    ├── Depends on Backend Routes
    └── Displays Data from Backend
    
Backend (Flask/Python)
    ├── Depends on Database
    ├── Manages File System
    └── Serves Frontend Templates
    
Database (SQLite)
    └── Stores User Data & Metadata
    
File System
    └── Stores Uploaded Photos
```

---

## 7. Security in Modules

### 7.1 Authentication Module
- Password hashing with Werkzeug
- Session validation on each protected route
- CSRF token ready (can be implemented)

### 7.2 File Upload Module
- File type validation
- File size validation
- Filename sanitization
- User-specific directories

### 7.3 Database Module
- Parameterized queries (SQL injection prevention)
- Foreign key constraints
- User data isolation

---

## 8. Module Testing Strategy

### 8.1 Backend Testing
- Test each route with valid/invalid input
- Test authentication flows
- Test file upload validation
- Test database operations
- Test error handling

### 8.2 Frontend Testing
- Test form validation
- Test responsive design
- Test JavaScript functionality
- Test cross-browser compatibility
- Test on mobile devices

### 8.3 Integration Testing
- Test complete workflows
- Test data flow between modules
- Test session management
- Test file storage and retrieval

---

## 9. Module Performance Optimization

### 9.1 Backend
- Use indexed database columns
- Implement query optimization
- Use caching for frequently accessed data
- Minimize database calls

### 9.2 Frontend
- Lazy load images
- Debounce search functionality
- Minimize CSS/JS files (for production)
- Use browser caching

### 9.3 Database
- Use proper indexing
- Optimize queries
- Archive old data (future)
- Use connection pooling (for production)

---

## 10. Module Scalability

### Current Limitations
- SQLite: Limited to single writer
- File system storage: Not scalable
- Single server: No load balancing

### Future Improvements
- Migrate to PostgreSQL
- Implement cloud storage (AWS S3)
- Add caching layer (Redis)
- Microservices architecture
- Load balancing

---

## Conclusion

The Cloud Photo Backup App is organized into well-defined modules that interact cohesively to provide a complete photo backup solution. Each module has clear responsibilities and interfaces, making the application maintainable, scalable, and easy to understand.

---

**Modules Documentation Version**: 1.0
**Status**: Complete
**Last Updated**: 2026
