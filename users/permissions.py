from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет являться ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsNotModer(permissions.BasePermission):
    """Проверка на то что пользователь не являться модератором"""
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moderator").exists()


class IsCreator(permissions.BasePermission):
    """Проверяет являться ли пользователь создателем объекта"""
    def has_odject_permission(self, request, view, odj):
        if odj.creator == request.user:
            return True
        return False
