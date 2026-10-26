from django.conf import settings
from django.db import models


class Pengaduan(models.Model):
    class Status(models.TextChoices):
        MENUNGGU = "menunggu", "Menunggu"
        DIPROSES = "diproses", "Diproses"
        SELESAI = "selesai", "Selesai"
        DITOLAK = "ditolak", "Ditolak"

    class Kategori(models.TextChoices):
        AKADEMIK = "akademik", "Akademik"
        FASILITAS = "fasilitas", "Fasilitas"
        ADMINISTRASI = "administrasi", "Administrasi"
        LAINNYA = "lainnya", "Lainnya"

    mahasiswa = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="pengaduan"
    )
    judul = models.CharField(max_length=150)
    kategori = models.CharField(max_length=20, choices=Kategori.choices, default=Kategori.LAINNYA)
    isi = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MENUNGGU)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-dibuat_pada"]

    def __str__(self):
        return f"#{self.pk} - {self.judul}"


class Tanggapan(models.Model):
    pengaduan = models.ForeignKey(Pengaduan, on_delete=models.CASCADE, related_name="tanggapan")
    petugas = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="tanggapan_diberikan"
    )
    isi = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["dibuat_pada"]

    def __str__(self):
        return f"Tanggapan untuk pengaduan #{self.pengaduan_id}"


class RiwayatStatus(models.Model):
    pengaduan = models.ForeignKey(Pengaduan, on_delete=models.CASCADE, related_name="riwayat")
    status_sebelumnya = models.CharField(max_length=20, blank=True)
    status_baru = models.CharField(max_length=20, choices=Pengaduan.Status.choices)
    catatan = models.CharField(max_length=255, blank=True)
    diubah_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="riwayat_status"
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-dibuat_pada"]

    def __str__(self):
        return f"Riwayat #{self.pengaduan_id}: {self.status_baru}"
