from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pengaduan, Tanggapan, RiwayatStatus
from .serializers import PengaduanSerializer, TanggapanSerializer, RiwayatStatusSerializer
from .permissions import PengaduanPermission


def beranda(request):
    return render(request, "pengaduan/beranda.html")


class PengaduanViewSet(viewsets.ModelViewSet):
    serializer_class = PengaduanSerializer
    permission_classes = [IsAuthenticated, PengaduanPermission]

    def get_queryset(self):
        qs = Pengaduan.objects.select_related("mahasiswa").prefetch_related("tanggapan", "riwayat")
        if self.request.user.is_staff:
            return qs
        return qs.filter(mahasiswa=self.request.user)

    def perform_create(self, serializer):
        item = serializer.save(mahasiswa=self.request.user)
        RiwayatStatus.objects.create(
            pengaduan=item, status_sebelumnya="", status_baru=item.status,
            catatan="Pengaduan dibuat", diubah_oleh=self.request.user
        )

    def update(self, request, *args, **kwargs):
        # Mahasiswa tidak boleh mengubah isi/status setelah pengaduan dibuat.
        if not request.user.is_staff:
            return Response({"detail": "Hanya admin yang dapat memperbarui pengaduan."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Hanya admin yang dapat memperbarui pengaduan."},
                            status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        status_lama = instance.status
        response = super().partial_update(request, *args, **kwargs)
        instance.refresh_from_db()
        if response.status_code < 300 and status_lama != instance.status:
            RiwayatStatus.objects.create(
                pengaduan=instance, status_sebelumnya=status_lama,
                status_baru=instance.status, catatan=request.data.get("catatan", ""),
                diubah_oleh=request.user
            )
        return response

    @action(detail=True, methods=["get", "post"], permission_classes=[IsAuthenticated])
    def tanggapan(self, request, pk=None):
        item = self.get_object()
        if not request.user.is_staff and item.mahasiswa_id != request.user.id:
            return Response({"detail": "Tidak diizinkan."}, status=403)
        if request.method == "GET":
            return Response(TanggapanSerializer(item.tanggapan.all(), many=True).data)
        if not request.user.is_staff:
            return Response({"detail": "Hanya admin/petugas yang dapat memberi tanggapan."}, status=403)
        serializer = TanggapanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(pengaduan=item, petugas=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def riwayat(self, request, pk=None):
        item = self.get_object()
        if not request.user.is_staff and item.mahasiswa_id != request.user.id:
            return Response({"detail": "Tidak diizinkan."}, status=403)
        return Response(RiwayatStatusSerializer(item.riwayat.all(), many=True).data)
