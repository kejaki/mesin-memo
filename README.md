# Media Moklet - Hub Manajemen Terintegrasi

Platform manajemen terintegrasi untuk Media Moklet yang powerful dan modern dengan Django.

## 🚀 Fitur Utama

### 1. Sistem Autentikasi & Keanggotaan
- ✅ Model User Custom dengan field Division, Class, NISN, dan Angkatan
- ✅ Registrasi & Login dengan verifikasi otomatis
- ✅ Dashboard Profil dengan badge "Verified Member"
- ✅ Fungsi Edit Profil lengkap
- ✅ User Groups (Admin, Coordinator, Member) dengan permission berbeda
- ✅ Halaman Anggota per Angkatan (33, 34, 35, dst)

### 2. Content Management System (CMS)
- ✅ Dashboard Kanban untuk perencanaan konten
- ✅ Form pembuatan konten (Judul, Platform, Jenis, Target Date)
- ✅ Sistem credit otomatis (Author, Editor, Designer)
- ✅ Status workflow: Idea → In Progress → Review → Final → Uploaded
- ✅ Badge platform (Instagram, YouTube, TikTok, Website)
- ✅ Jenis konten: Motanya, Melapor, Podcast, Bemo, Besmo, IG Story

### 3. Gamifikasi
- ✅ Leaderboard dengan visual ranking
- ✅ Sistem poin otomatis:
  - Author: 100 XP
  - Designer: 100 XP
  - Editor: 50 XP
- ✅ Verified Badge untuk member aktif

### 4. Manajemen Event
- ✅ Kalender event (Upcoming & Past)
- ✅ Tracking kebutuhan liputan (Foto, Video, Artikel)
- ✅ Assignment koordinator event
- ✅ Link dokumentasi
- ✅ Form pembuatan event baru

### 5. Divisi
Sistem divisi baru dengan 3 kategori:
- **Jurnalistik** - Reporter, penulis artikel
- **Design** - Desainer grafis, visual creator
- **Fotografi** - Fotografer, videografer

## 🛠️ Tech Stack

- **Backend**: Django 5.2
- **Frontend**: Tailwind CSS + Alpine.js
- **Database**: SQLite (development) / PostgreSQL (production)
- **Font**: Google Fonts - Outfit
- **Color Scheme**: Hijau cerah (Green)

## 📦 Instalasi & Setup

### 1. Clone & Navigate
```bash
cd /path/to/media_moklet
```

### 2. Aktifkan Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies (jika belum)
```bash
pip install django
```

### 4. Jalankan Migrasi Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Setup User Groups (Satu kali saja)
```bash
python manage.py setup_groups
```

### 6. Buat Superuser (jika belum ada)
```bash
python manage.py createsuperuser
```

### 7. Jalankan Development Server
```bash
python manage.py runserver
```

Akses di: `http://127.0.0.1:8000/`

## 🔑 Default Admin Credentials

Jika sudah dibuat sebelumnya:
- **Username**: `admin`
- **Password**: `admin123`

## 📍 URL Penting

- **Homepage**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **CMS Dashboard**: `http://127.0.0.1:8000/cms/dashboard/`
- **Leaderboard**: `http://127.0.0.1:8000/auth/leaderboard/`
- **Events**: `http://127.0.0.1:8000/events/`
- **Create Event**: `http://127.0.0.1:8000/events/create/`
- **Create Content**: `http://127.0.0.1:8000/cms/create/`
- **Edit Profile**: `http://127.0.0.1:8000/auth/profile/edit/`
- **Angkatan 33**: `http://127.0.0.1:8000/auth/angkatan/33/`
- **Angkatan 34**: `http://127.0.0.1:8000/auth/angkatan/34/`

## 🎨 Fitur Desain

- Navbar glassmorphism dengan efek blur
- Animasi smooth fade-in
- Efek hover interaktif
- Gradient button modern
- Desain responsive (mobile-first)
- Color scheme hijau cerah

## 👥 Workflow Manajemen User

1. **User mendaftar** → Status: "Pending"
2. **Admin verifikasi** via Admin Panel
3. **User dapat "Verified Badge"**
4. **Admin assign group** (Member/Coordinator/Admin)
5. **User mendapat permission** sesuai role

## 📊 Workflow Konten

1. Member membuat ide konten
2. Admin/Coordinator assign tim (Author, Editor, Designer)
3. Konten bergerak melalui status
4. Saat di-mark "Uploaded" → XP otomatis diberikan
5. Leaderboard terupdate otomatis

## 🔧 Struktur Project

```
media_moklet/
├── config/              # Django settings
├── core/                # Homepage & base templates
├── users/               # Authentication & profiles
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py
│   ├── templates/users/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   ├── edit_profile.html
│   │   ├── leaderboard.html
│   │   └── members_angkatan.html
│   ├── models.py        # Custom User Model (with angkatan)
│   ├── forms.py
│   ├── views.py
│   └── admin.py         # Admin actions
├── cms/                 # Content Management
│   ├── templates/cms/
│   │   ├── dashboard.html
│   │   └── create_content.html
│   ├── models.py        # ContentItem model
│   ├── signals.py       # Auto-points logic
│   └── admin.py
├── events/              # Event Management
│   ├── templates/events/
│   │   ├── event_list.html
│   │   └── create_event.html
│   ├── models.py
│   ├── forms.py
│   └── admin.py
├── db.sqlite3
├── manage.py
└── README.md
```

## 🎯 Admin Panel - Aksi Bulk

Admin memiliki beberapa **Bulk Actions** untuk mempermudah manajemen:

### User Management
1. **Verify selected users** - Verifikasi member sekaligus
2. **Remove verification** - Hapus status verifikasi
3. **Add to Member group** - Tambahkan ke grup Member
4. **Change division → Jurnalistik** - Ubah divisi ke Jurnalistik
5. **Change division → Design** - Ubah divisi ke Design
6. **Change division → Fotografi** - Ubah divisi ke Fotografi

### Cara Menggunakan:
1. Buka Admin Panel `/admin/`
2. Pilih **Users**
3. Centang user yang ingin diubah
4. Pilih action dari dropdown
5. Klik **"Go"**

## 📝 Menambah Jenis Konten Baru

Untuk menambahkan jenis konten baru:

1. **Edit file**: `cms/models.py`
2. Tambahkan di `class Type(models.TextChoices)`:
   ```python
   NAMA_BARU = 'NAMA_BARU', 'Display Name'
   ```
3. Jalankan migrasi:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 🔄 Menambah Angkatan Baru

Angkatan ditambahkan otomatis saat:
- User mendaftar dengan angkatan tertentu
- Admin mengedit angkatan di Admin Panel

Untuk menampilkan di homepage, edit: `core/templates/core/home.html`

## 🚀 Pengembangan Selanjutnya

### Fitur yang Bisa Ditambahkan:

1. **Notifikasi Real-time**
   - Gunakan Django Channels untuk WebSocket
   - Notifikasi saat di-assign task
   - Notifikasi saat content approved

2. **File Upload**
   - Tambahkan field `FileField` di ContentItem
   - Konfigurasi `MEDIA_ROOT` dan `MEDIA_URL`
   - Setup storage (AWS S3/Cloudinary untuk production)

3. **Calendar Widget Dinamis**
   - Integrasi FullCalendar.js
   - Tampilkan event dan deadline konten
   - Drag & drop untuk reschedule

4. **Analytics Dashboard**
   - Grafik kontribusi per divisi
   - Trend content type
   - Member growth chart

5. **Export Report**
   - Export data content ke Excel
   - PDF report untuk evaluasi bulanan

6. **Email Notifications**
   - Setup SMTP di settings.py
   - Kirim email saat verifikasi
   - Reminder deadline konten

## 🔐 Keamanan untuk Production

Sebelum deploy ke production:

1. **Environment Variables**
   ```python
   # settings.py
   SECRET_KEY = os.environ.get('SECRET_KEY')
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Database Production**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'mediamoklet',
           'USER': 'dbuser',
           'PASSWORD': os.environ.get('DB_PASSWORD'),
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **HTTPS**
   - Setup SSL certificate
   - Konfigurasi SECURE_SSL_REDIRECT

## 🐛 Troubleshooting

### Port 8000 sudah digunakan
```bash
# Cari process yang menggunakan port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
# Atau gunakan port lain
python manage.py runserver 8001
```

### Migration Error
```bash
# Hapus cache migrasi
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
# Buat ulang
python manage.py makemigrations
python manage.py migrate
```

### Admin CSS tidak muncul
```bash
python manage.py collectstatic --clear
```

## 📚 Dokumentasi Django

Untuk referensi lebih lanjut:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)
- [Django Signals](https://docs.djangoproject.com/en/5.2/topics/signals/)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 👨‍💻 Development Tips

1. **Gunakan Virtual Environment**
   - Selalu aktifkan venv sebelum coding
   - Install package di venv, bukan global

2. **Git Version Control**
   ```bash
   git add .
   git commit -m "feat: deskripsi fitur"
   git push origin main
   ```

3. **Make Migrations Reguler**
   - Setiap ubah model → makemigrations
   - Test di development dulu

4. **Admin Panel sebagai Quick Tool**
   - Gunakan admin untuk testing cepat
   - Buat sample data via admin

## 🎓 Kontributor

Website ini dikembangkan untuk Media Moklet SMK Telkom Malang.

---

**Happy Coding! 🚀**

Untuk pertanyaan atau bug report, buka issue di repository atau hubungi tim developer.
# media-moklet
