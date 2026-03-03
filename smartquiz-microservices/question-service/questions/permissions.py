from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        print("ROLE:", request.user.role)
        if not request.user:
            return False

        role = getattr(request.user, "role", None)

        if role and role.lower() == "admin":
            return True

        return False