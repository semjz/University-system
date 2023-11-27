import datetime

from rest_framework import permissions
from rolepermissions.checkers import has_role

from authentication.roles import AssistantRole, StudentRole
from management.models import Faculty


class IsCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        school_ids = request.data["schools"]
        for school_id in school_ids:
            school = Faculty.objects.get(id=school_id)
            if request.user.id != school.assistant.user_id:
                return False
        return True


class IsAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, AssistantRole)


class IsSameStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, StudentRole)

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id
