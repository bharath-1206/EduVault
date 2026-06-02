# 🎓 EduVault

**EduVault** is a secure, role-based academic material management system designed for colleges to efficiently manage, upload, and access study materials across departments and semesters.

---

## 🚀 Overview

EduVault streamlines the distribution of academic resources by implementing a structured **Role-Based Access Control (RBAC)** system. It ensures that only authorized users can upload, view, or manage materials based on their role and academic structure.

---

## 🎯 Key Features

### 🔐 Authentication & Security

* Secure authentication and session management
* Role-Based Access Control (RBAC)
* Controlled academic access
* Protected resource visibility

### 👨‍🏫 Role-Based System

#### **HOD (Head of Department)**

* Manage staff
* Upload / view / delete branch materials
* View activity logs

#### **Branch Staff**

* Access materials for assigned branch (Sem 3+)
* Upload subject-specific resources

#### **Cycle Staff**

* Access common cycle materials (Sem 1 & 2)

#### **Students**

* View materials based on semester and branch

---

## 📂 Material Management

* Upload academic resources
* PDF and file management
* Organized by:

  * Branch
  * Semester
  * Subject
* Cloud media storage using Cloudinary
* Controlled visibility using RBAC

---

## 🧠 Smart Access Logic

EduVault ensures:

* Cycle materials (Sem 1 & 2) → Accessible only to cycle users
* Branch materials (Sem 3+) → Controlled branch access
* HOD access:

  * All branch materials
  * Self-uploaded materials

---

## 📊 Activity Logging

Tracks:

* Uploads
* Deletions
* Logins

Administrative controls:

* View logs
* Manage logs

---

## 🖥️ User Interface

* Bootstrap dashboard UI
* Responsive design
* Sidebar navigation
* Custom branding

---

## ⚙️ Tech Stack

| Layer      | Technology           |
| ---------- | -------------------- |
| Backend    | Django 6             |
| Frontend   | HTML, CSS, Bootstrap |
| Database   | Supabase PostgreSQL  |
| Storage    | Cloudinary           |
| Deployment | Railway              |
| Server     | Gunicorn             |

---

## 🏗️ Architecture

```text
GitHub
 ↓
Railway
 ↓
Django
 ↓
Supabase PostgreSQL
 ↓
Cloudinary
```

---

## 🗂️ Project Structure

```text
EduVault/
│
├── eduvault/
│   ├── academics/
│   ├── accounts/
│   ├── staff/
│   ├── students/
│   ├── materials/
│   ├── templates/
│   ├── staticfiles/
│   ├── eduvault/
│   ├── manage.py
│   └── requirements.txt
```

---

## 🔧 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-repo/eduvault.git
cd EduVault/eduvault
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create:

```text
.env
```

Add:

```env
DATABASE_URL=

SECRET_KEY=

DEBUG=True

CLOUDINARY_CLOUD_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=
```

---

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🌐 Deployment

Hosted on Railway.

Environment variables:

```env
DATABASE_URL=

SECRET_KEY=

DEBUG=False

CLOUDINARY_CLOUD_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=
```

---

## 🎨 Branding

Custom branding includes:

* Login page logo
* Dashboard logo
* Browser favicon

---

## 🔒 Security Highlights

* Session-based authentication
* Role-based authorization
* Environment isolation
* Controlled resource access

---

## 📌 Future Enhancements

* Password reset
* Notifications
* Mobile optimization
* Analytics dashboard
* Material versioning

---

## 👨‍💻 Contributors

* Mohan Gowda B L
* Bharath M

---

## ⭐ Conclusion

EduVault is designed to solve real-world academic material distribution challenges by combining **security, structure, and scalability** into a single platform.

---

> **"Structured access leads to efficient learning."**
