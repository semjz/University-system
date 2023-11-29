from rest_framework import permissions
from rolepermissions.checkers import has_role

from authentication.roles import ITManager


class IsItManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, ITManager)

