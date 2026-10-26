# SIMPEL — Sistem Pengaduan Mahasiswa berbasis REST API

Proyek pembelajaran menggunakan Django, Django REST Framework, dan SQLite.

## Kebutuhan
- Python 3.10 atau lebih baru yang kompatibel dengan versi Django terpasang
- VS Code
- Postman (opsional, untuk menguji API)

## Menjalankan di Windows
Buka terminal VS Code di folder proyek.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Jika PowerShell memblokir aktivasi, gunakan terminal CMD:
```cmd
venv\Scripts\activate.bat
```

Buka:
- Beranda: http://127.0.0.1:8000/
- REST API: http://127.0.0.1:8000/api/
- Panel admin: http://127.0.0.1:8000/admin/

## Endpoint utama
- `GET /api/pengaduan/` — daftar pengaduan milik pengguna; staff dapat melihat semua
- `POST /api/pengaduan/` — membuat pengaduan
- `GET /api/pengaduan/{id}/` — detail pengaduan
- `GET /api/pengaduan/{id}/tanggapan/` — melihat tanggapan
- `POST /api/pengaduan/{id}/tanggapan/` — staff/admin memberi tanggapan
- `GET /api/pengaduan/{id}/riwayat/` — riwayat status
- `PATCH /api/pengaduan/{id}/` — staff/admin memperbarui status, contoh body: `{"status":"diproses","catatan":"Sedang diperiksa"}`

## Login dan hak akses
Gunakan `/api/auth/login/` untuk login melalui browsable API. Akun staff dibuat lewat `createsuperuser`. Pengguna biasa dapat dibuat melalui panel admin atau shell Django.

## Contoh membuat pengaduan
Login sebagai pengguna terlebih dahulu di browsable API atau gunakan Basic Auth di Postman. Kirim `POST /api/pengaduan/` dengan JSON:

```json
{
  "judul": "Lampu ruang kelas mati",
  "kategori": "fasilitas",
  "isi": "Lampu di ruang kelas tidak menyala sejak kemarin."
}
```

Status awal otomatis `menunggu`; catatan awal masuk ke riwayat.

## Catatan penting
- Database `db.sqlite3` dibuat saat menjalankan `python manage.py migrate`, sehingga tidak disertakan sebagai database awal.
- `DEBUG=True` dan `SECRET_KEY` pada pengaturan ini hanya untuk pengembangan lokal. Jangan gunakan konfigurasi tersebut langsung di server publik.
- Untuk demo tugas, gunakan data contoh dan jangan memasukkan data sensitif mahasiswa.
