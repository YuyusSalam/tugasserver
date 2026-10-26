from rest_framework import serializers
from .models import Pengaduan, Tanggapan, RiwayatStatus


class TanggapanSerializer(serializers.ModelSerializer):
    nama_petugas = serializers.CharField(source="petugas.username", read_only=True)

    class Meta:
        model = Tanggapan
        fields = ["id", "pengaduan", "petugas", "nama_petugas", "isi", "dibuat_pada"]
        read_only_fields = ["id", "pengaduan", "petugas", "nama_petugas", "dibuat_pada"]


class RiwayatStatusSerializer(serializers.ModelSerializer):
    nama_pengubah = serializers.CharField(source="diubah_oleh.username", read_only=True)

    class Meta:
        model = RiwayatStatus
        fields = [
            "id", "pengaduan", "status_sebelumnya", "status_baru",
            "catatan", "diubah_oleh", "nama_pengubah", "dibuat_pada"
        ]
        read_only_fields = fields


class PengaduanSerializer(serializers.ModelSerializer):
    nama_mahasiswa = serializers.CharField(source="mahasiswa.username", read_only=True)
    tanggapan = TanggapanSerializer(many=True, read_only=True)
    riwayat = RiwayatStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Pengaduan
        fields = [
            "id", "mahasiswa", "nama_mahasiswa", "judul", "kategori", "isi",
            "status", "dibuat_pada", "diperbarui_pada", "tanggapan", "riwayat"
        ]
        read_only_fields = [
            "id", "mahasiswa", "nama_mahasiswa",
            "dibuat_pada", "diperbarui_pada", "tanggapan", "riwayat"
        ]

    def validate_status(self, value):
        request = self.context.get("request")
        if request and not request.user.is_staff:
            raise serializers.ValidationError("Hanya admin/petugas yang dapat mengubah status.")
        return value
