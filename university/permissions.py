from rest_framework import permissions


class IsItManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="IT Manager")
