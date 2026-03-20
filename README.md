# 📚 EduVault

EduVault is a **Django-based academic resource management system** designed for colleges to manage, upload, and access study materials efficiently.

---

## 🚀 Features

### 👨‍🎓 Student Module
- Login using **USN (no password required)**
- Automatically detects:
  - 📘 Scheme from USN  
  - 🏫 Branch from USN  
- View materials by:
  - Semester  
  - Subject  
- Clean dashboard UI for easy navigation  

---

### 👨‍🏫 Staff Module
- Login using **Staff ID + Password**
- Admin-controlled access:
  - ✅ Active → full access  
  - ❌ Inactive → login blocked  
- Upload materials:
  - PDF, PPT, DOC supported  
- Delete uploaded materials  
- View materials filtered by branch  

---

### 🔐 Authentication System
- Hybrid login system:
  - Students → direct login  
  - Staff → password-based login  
- Session-based authentication  
- Auto logout system:
  - Logs out after inactivity  
  - Timer resets on user activity  

---

### ☁️ File Storage
- Integrated with **Cloudinary**
- Supports:
  - PDF  
  - PPT / PPTX  
  - DOC / DOCX  
- Files are stored securely in the cloud  
- No dependency on local `/media`  

---

### 📊 Activity Logging System
- Tracks all important actions:
  - 📁 Material upload  
  - ❌ Material deletion  
  - 👨‍🎓 Student creation  
- Stores:
  - User type (admin/staff)  
  - User ID  
  - Action performed  
  - Timestamp  
- Accessible **only via Django Admin panel**
- Logs are **read-only (cannot be modified/deleted)**  

---

### 🛡️ Security Features
- Staff account activation control  
- Session protection (no direct URL access)  
- Auto logout after inactivity  
- Admin-only access to logs  

---

## 🏗️ Tech Stack

- **Backend:** Django (Python)  
- **Database:** PostgreSQL (Render) / SQLite (local)  
- **Frontend:** HTML, Bootstrap  
- **Cloud Storage:** Cloudinary  
- **Deployment:** Render  

---

## ⚙️ Installation (Local Setup)

```bash
# Clone repository
git clone https://github.com/your-username/EduVault.git
cd EduVault

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver

## 🔑 Admin Access

Create a superuser:

```bash
python manage.py createsuperuser

Access the Django admin panel:

http://127.0.0.1:8000/admin/
👑 Admin Capabilities

The admin panel provides full control over the system:

🧑‍🎓 Student Management

Add new students manually

Automatically detects:

Scheme from USN

Branch from USN

View and manage all registered students

👨‍🏫 Staff Management

Add new staff members

Assign:

Staff ID

Password

Branch

Enable / Disable staff access:

✅ Active → can login

❌ Inactive → login blocked

📚 Materials Management

View all uploaded materials

Organized by:

Subject

Branch

Delete inappropriate or outdated materials

📊 Activity Logs (Audit System)

View all system activities in one place

Tracks:

📁 Material uploads

❌ Material deletions

👨‍🎓 Student registrations

Displays:

User type (admin / staff)

User ID

Action performed

Timestamp

🔒 Log Security

Logs are read-only

Cannot be edited or deleted manually

Only accessible through the admin panel

🔍 Admin Features

Search logs by user or action

Filter logs by:

User type

Date/time

Sorted by latest activity

📂 Project Structure
EduVault/
│
├── accounts/      # Authentication & logging
├── students/      # Student model & logic
├── staff/         # Staff dashboard & upload system
├── materials/     # Study materials
├── academics/     # Scheme, semester, subjects
├── templates/     # HTML templates
├── static/        # CSS, JS
│
└── manage.py
🌐 Deployment

EduVault is deployed on Render.

Uses PostgreSQL database

Cloudinary for media storage

Static files served via WhiteNoise

🔥 Future Enhancements

🔍 Search materials

👁️ PDF preview inside dashboard

📊 Download analytics

🔐 Password hashing for staff

📱 Mobile responsive UI improvements

📅 Advanced log filtering

👨‍💻 Author

Mohan Gowda B L

📜 License

This project is for educational use.

⭐ If you like this project, consider giving it a star!