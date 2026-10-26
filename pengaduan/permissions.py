from rest_framework.permissions import BasePermission, SAFE_METHODS


class PengaduanPermission(BasePermission):
    """
    Pengguna yang login hanya melihat/mengelola pengaduannya sendiri.
    Staff/admin boleh melihat semua pengaduan dan mengubah status.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.mahasiswa_id == request.user.id and request.method in SAFE_METHODS
