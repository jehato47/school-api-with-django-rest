from rest_framework import permissions


# todo: Gereken yerlere ekle
class Issuperuser(permissions.BasePermission):
    message = {"success": False, "error": "Yönetici Değilsiniz"}

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


# todo: Gereken yerlere ekle
class Isstaff(permissions.BasePermission):
    message = {"success": False, "error": "Öğretmen Değilsiniz"}

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


# todo: Gereken yerlere ekle
class HaveData(permissions.BasePermission):
    message = {"success": False, "error": "Veri Göndermelisiniz"}

    def has_permission(self, request, view):
        if request.data:
            return True
        return False


class OnlyTeacher(permissions.BasePermission):
    message = {"success": False, "error": "Öğretmen değilsiniz"}

    def has_permission(self, request, view):
        u = request.user
        if u.is_staff and not u.is_superuser:
            return True
        return False
