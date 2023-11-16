from rest_framework import permissions


class IsItManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "it-manager"
