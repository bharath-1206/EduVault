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

EduVault is configured for deployment on Render as a Django Web Service. The project uses PostgreSQL through `DATABASE_URL`, WhiteNoise for static files, and Cloudinary for uploaded media.

Render configuration is included in `render.yaml` and `eduvault/build.sh`.

Environment variables:

```env
DATABASE_URL=

SECRET_KEY=

DEBUG=False

CLOUDINARY_CLOUD_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=

ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
```

For a Render deployment, set `ALLOWED_HOSTS` to the Render hostname (for example, `eduvault.onrender.com`) and `CSRF_TRUSTED_ORIGINS` to the full HTTPS origin (for example, `https://eduvault.onrender.com`).

### Render commands

The repository contains a Render build script that installs dependencies, collects static files, and runs migrations. The web service starts with Gunicorn bound to Render's `$PORT`.

A lightweight `/health/` endpoint is included for Render health checks and external uptime monitoring.

### Keeping the free service awake

Render Free web services normally spin down after 15 minutes without inbound traffic. This repository includes an optional GitHub Actions workflow at `.github/workflows/keep-render-awake.yml` that pings `/health/` every 10 minutes. Configure the repository secret `RENDER_HEALTH_URL` with the complete health URL.

This is optional and consumes nearly all of the free monthly instance-hours when used continuously, so it is better suited to a demo/project deployment than a production service.

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
