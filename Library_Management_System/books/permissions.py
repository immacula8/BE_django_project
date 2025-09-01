from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only for everyone; write actions only for staff/superuser.
    """
    def has_permission(self, request, view):
        # safe methods are allowed for anyone (read)
        if request.method in permissions.SAFE_METHODS:
            return True
        # write methods require authenticated staff or superuser
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))
