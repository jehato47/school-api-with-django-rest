from rest_framework import permissions


class Issuperuser(permissions.BasePermission):
    message = {"success": False, "error": "Yönetici Değilsiniz"}

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class Isstaff(permissions.BasePermission):
    message = {"success": False, "error": "Öğretmen Değilsiniz"}

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class HaveData(permissions.BasePermission):
    message = {"success": False, "error": "Veri Göndermelisiniz"}

    def has_permission(self, request, view):
        if request.data:
            return True
        return False
