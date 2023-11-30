import datetime

from rest_framework import permissions
from rolepermissions.checkers import has_role

from authentication.roles import AssistantRole, StudentRole
from management.models import Faculty


class IsCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        school_names = request.data["schools"]
        for school_name in school_names:
            school = Faculty.objects.get(name=school_name)
            if request.user.id != school.assistant.user_id:
                return False
        return True


class IsTermCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        course = request.data["course"]
        for school in course.schools:
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
