from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.use and request.use.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class ReadOnlyForAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action == ['list', 'retrieve']:
            return request.user.is_authenticated or request.user.is_staff
        elif view.action in ['update', 'partial_update', 'destroy', 'create']:
            return request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == ['retrieve', 'list']:
            return obj == request.user.is_authenticated or request.user.is_staff
        elif view.action in ['update', 'partial_update', 'destroy', 'create']:
            return request.user.is_staff
        else:
            return False
