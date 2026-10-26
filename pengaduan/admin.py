from django.contrib import admin
from .models import Pengaduan, Tanggapan, RiwayatStatus


class TanggapanInline(admin.TabularInline):
    model = Tanggapan
    extra = 0
    readonly_fields = ["dibuat_pada"]


class RiwayatInline(admin.TabularInline):
    model = RiwayatStatus
    extra = 0
    readonly_fields = ["status_sebelumnya", "status_baru", "catatan", "diubah_oleh", "dibuat_pada"]
    can_delete = False


@admin.register(Pengaduan)
class PengaduanAdmin(admin.ModelAdmin):
    list_display = ["id", "judul", "mahasiswa", "kategori", "status", "dibuat_pada"]
    list_filter = ["status", "kategori", "dibuat_pada"]
    search_fields = ["judul", "isi", "mahasiswa__username"]
    list_editable = ["status"]
    inlines = [TanggapanInline, RiwayatInline]


@admin.register(Tanggapan)
class TanggapanAdmin(admin.ModelAdmin):
    list_display = ["id", "pengaduan", "petugas", "dibuat_pada"]


@admin.register(RiwayatStatus)
class RiwayatStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "pengaduan", "status_sebelumnya", "status_baru", "diubah_oleh", "dibuat_pada"]
    readonly_fields = ["pengaduan", "status_sebelumnya", "status_baru", "catatan", "diubah_oleh", "dibuat_pada"]
