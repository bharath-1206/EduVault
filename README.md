# 🎓 EduVault

**EduVault** is a secure, role-based academic material management system designed for colleges to efficiently manage, upload, and access study materials across departments and semesters.

---

## 🚀 Overview

EduVault streamlines the distribution of academic resources by implementing a structured **Role-Based Access Control (RBAC)** system. It ensures that only authorized users can upload, view, or manage materials based on their role and academic structure.

---

## 🎯 Key Features

### 🔐 Authentication & Security

- Secure login using Django authentication system  
- Password hashing and session management  
- Role-based access control (RBAC)  

### 👨‍🏫 Role-Based System

#### **HOD (Head of Department)**
- Manage staff  
- Upload/view/delete branch materials  
- View activity logs  

#### **Branch Staff**
- Access materials for their branch (Sem 3+)  
- Upload subject-specific resources  

#### **Cycle Staff**
- Access common cycle materials (Sem 1 & 2)  

#### **Students**
- View materials based on their semester and branch  

---

## 📂 Material Management

- Upload materials (PDFs, files)  
- Organized by:  
  - Branch  
  - Semester  
  - Subject  
- Cloud storage integration using **Cloudinary**  
- Controlled visibility based on role + ownership  

---

## 🧠 Smart Access Logic

EduVault ensures:

- Cycle materials (Sem 1 & 2) → Only cycle staff & relevant users  
- Branch materials (Sem 3+) → Only branch staff & HOD  
- HOD can access:  
  - All branch materials  
  - Materials uploaded by themselves  

---

## 📊 Activity Logging

- Tracks system actions such as:  
  - Uploads  
  - Deletions  
  - Logins  

- Admin can:  
  - View logs  
  - Delete logs (controlled access)  

---

## 🖥️ User Interface

- Clean dashboard UI using **Bootstrap**  
- Sidebar navigation  
- Responsive design  
- Custom branding with logo integration  

---

## ⚙️ Tech Stack

| Layer      | Technology            |
|------------|----------------------|
| Backend    | Django 6             |
| Frontend   | HTML, CSS, Bootstrap |
| Database   | PostgreSQL / SQLite  |
| Storage    | Cloudinary           |
| Deployment | Render               |
| Server     | Gunicorn + WhiteNoise|

---

## 🗂️ Project Structure

```
EduVault/
│
├── accounts/        # Authentication & activity logs  
├── staff/           # Staff management & RBAC  
├── students/        # Student data  
├── materials/       # Material upload & access  
├── academics/       # Subjects, semesters, branches  
├── eduvault/        # Core settings & configuration  
├── templates/       # HTML templates  
├── static/          # Static files (logo, CSS)  
```

---

## 🔧 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-repo/eduvault.git
cd eduvault
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🌐 Deployment

- Hosted on **Render**  
- Uses:  
  - PostgreSQL database  
  - WhiteNoise for static files  
  - Gunicorn for production server  

---

## 🎨 Branding

- Custom logo integrated across:  
  - Login page  
  - Dashboard  
  - Browser favicon  

---

## 🔒 Security Highlights

- Django built-in authentication  
- Hashed passwords  
- Session expiration handling  
- Role-based access restrictions  

---

## 📌 Future Enhancements

- 🔄 Password reset via email  
- 📱 Mobile optimization  
- 📊 Analytics dashboard  
- 🔔 Notifications system  
- 📁 Version control for materials  

---

## 👨‍💻 Contributors

- **Mohan Gowda B L**  
- **Bharath M**  

---

## 📬 Contact

📧 mohanrgbl6629@gmail.com  

---

## ⭐ Conclusion

EduVault is designed to solve real-world academic material distribution challenges by combining **security, structure, and scalability** into a single platform.

---

> **“Structured access leads to efficient learning.”**  ``