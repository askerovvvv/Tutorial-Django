from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """
    Allows access only to admin users or is_teacher.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher or request.user.is_staff)

