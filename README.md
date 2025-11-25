# 📱 Media Moklet Hub

**Platform manajemen konten dan kolaborasi untuk Media Moklet SMK Telkom Malang**

Media Moklet Hub adalah sistem manajemen konten berbasis web yang dirancang khusus untuk tim Media Moklet. Platform ini memudahkan koordinasi pembuatan konten, penugasan role, tracking progress, dan gamifikasi kontribusi anggota.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-cyan)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fitur Utama

### 📋 Content Management System
- **Content Planning**: Create dan manage content plan dengan detail (judul, platform, tanggal target, deskripsi)
- **Job Roles System**: Assign specific roles (Cameraman, Video Editor, Caption Writer, etc.) untuk setiap konten
- **Dynamic Role Claiming**: Member bisa pilih role yang ingin diambil per konten
- **Progress Tracking**: Status tracking (Idea → In Progress → Review → Final → Uploaded)
- **Kanban Board**: Visual dashboard untuk melihat semua konten dengan status counting

### 👥 Role & Permission System
- **Badge System**: Assign badges ke user (PIC Divisi, Ketua memo, Waka, Sekretaris, dll)
- **Role-Based Permissions**:
  - **PIC Divisi**: Bisa create content dan events
  - **Ketua**: Bisa create events
  - **Member**: Bisa claim roles dan berkontribusi
- **Verification System**: Admin approve member baru sebelum bisa akses penuh

### 🏆 Gamification
- **XP System**: Dapatkan poin berdasarkan kontribusi
- **Role-Based XP**:
  - Video Editor: 150 XP
  - Cameraman: 120 XP
  - Content Writer: 100 XP
  - Talent: 100 XP
  - Thumbnail Designer: 90 XP
  - Caption Writer: 80 XP
- **Leaderboard**:
  - **Global**: Top 50 contributors
  - **Per Divisi**: Top 20 per divisi (Jurnalistik, Design, Fotografi)
  - **Per Angkatan**: Top 10 per angkatan

### 📅 Event Management
- Create dan manage events Media Moklet
- Dashboard display untuk upcoming events
- RSVP system
- Event calendar
- Participant tracking

### 👤 User Profile
- Upload foto profil
- Display badges
- Show total XP dan ranking
- Activity history
- Edit profile info

## 🛠️ Tech Stack

### Backend
- **Django 4.2**: Web framework
- **Python 3.13**: Programming language
- **SQLite**: Database (development)
- **Pillow**: Image processing

### Frontend
- **TailwindCSS**: UI framework
- **Alpine.js**: Lightweight JavaScript framework
- **Google Fonts (Outfit)**: Typography

### Features
- **Authentication**: Django built-in auth
- **File Upload**: Profile photos support
- **Middleware**: Custom verification & permission checks
- **Admin Panel**: Customized Django admin

## 📦 Installation

### Prerequisites
- Python 3.10+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd media_moklet
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Migrations**
```bash
python manage.py migrate
```

5. **Create Superuser**
```bash
python manage.py createsuperuser
```

6. **Create Predefined Badges**
```bash
python manage.py shell < create_badges.py
```

7. **Run Development Server**
```bash
python manage.py runserver
```

8. **Access Application**
- Main site: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## 📖 Usage Guide

### For Members

1. **Register Account**
   - Buka halaman register
   - Isi data: username, NISN, kelas, divisi, angkatan
   - Tunggu admin approve (set `is_verified=True`)

2. **Claim Job Roles**
   - Lihat job tersedia di menu "Jobs → Job Tersedia"
   - Klik detail content yang menarik
   - Pilih role yang ingin diambil
   - 1 user hanya bisa ambil 1 role per content

3. **Track Progress**
   - Lihat job yang diambil di "Jobs → Job Saya"
   - Check status content
   - Collaborate dengan team

4. **Earn XP**
   - Selesaikan konten
   - Admin set status ke "Uploaded"
   - XP otomatis masuk sesuai role
   - Check ranking di Leaderboard

### For PIC Divisi

1. **Create Content Plan**
   - Navigate ke "Content → Create"
   - Isi informasi content
   - Tambah job roles yang dibutuhkan:
     - Pilih role type
     - Set jumlah orang
     - Tambah deskripsi (optional)
   - Submit

2. **Manage Content**
   - Click content card untuk edit
   - Update status sesuai progress
   - Add/remove job roles
   - Monitor assignments

3. **Create Events**
   - Navigate ke "Events → Create Event"
   - Isi detail event
   - Set max participants (optional)

### For Admin

1. **Verify New Users**
   - Login ke admin panel
   - Users → User
   - Set `is_verified=True` untuk approve

2. **Assign Roles & Badges**
   - Edit user
   - Set "Role/Jabatan" (PIC_DIVISI, KETUA, etc.)
   - Assign badges sesuai kebutuhan

3. **Manage Badges**
   - Badges → Add badge
   - Set nama, icon (emoji), warna, deskripsi
   - Badge bisa di-assign ke banyak user

4. **Monitor Activity**
   - Check Activity Logs
   - View all content items
   - Monitor job assignments

## 📁 Project Structure

```
media_moklet/
├── config/              # Django settings
├── core/                # Core app (homepage, base templates)
├── users/               # User management, auth, profiles
│   ├── models.py       # User, Badge models
│   ├── views.py        # Profile, leaderboard
│   └── templates/      # Profile, leaderboard templates
├── cms/                 # Content Management System
│   ├── models.py       # ContentItem, JobRole, JobRoleAssignment
│   ├── views.py        # Content CRUD, role claiming
│   └── templates/      # Dashboard, content templates
├── events/              # Event management
├── media/               # Uploaded files (profile photos)
└── manage.py
```

## 🎯 Key Models

### User (users/models.py)
- Extends Django AbstractUser
- Fields: role, division, angkatan, profile_photo, badges (M2M), points
- Methods: `can_create_content()`, `can_create_event()`, `has_role()`

### Badge (users/models.py)
- Fields: name, slug, color, icon, description
- M2M relationship with User

### ContentItem (cms/models.py)
- Fields: title, content_type, platform, status, target_date, is_claimable
- Related: JobRole (1-to-many)

### JobRole (cms/models.py)
- Fields: role_type, slots_needed, description
- Related: JobRoleAssignment (1-to-many)
- Methods: `is_full()`, `get_slots_remaining()`

### JobRoleAssignment (cms/models.py)
- ForeignKeys: job_role, user
- Tracks who claimed which role

## 🔒 Permissions

| Action | Member | PIC Divisi | Ketua | Admin |
|--------|--------|------------|-------|-------|
| View Content | ✅ | ✅ | ✅ | ✅ |
| Create Content | ❌ | ✅ | ❌ | ✅ |
| Claim Roles | ✅ | ✅ | ✅ | ✅ |
| Create Events | ❌ | ✅ | ✅ | ✅ |
| Verify Users | ❌ | ❌ | ❌ | ✅ |
| Assign Badges | ❌ | ❌ | ❌ | ✅ |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

Developed for **Media Moklet SMK Telkom Malang**

## 📧 Support

For issues or questions, contact admin Media Moklet.

---

**⭐ Star this repo if you find it useful!**
