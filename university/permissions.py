from rest_framework import permissions


class IsItManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "it-manager"


class IsAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "assistant"
