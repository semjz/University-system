from rest_framework import permissions
from rolepermissions.checkers import has_role
from rest_framework import viewsets
from .models import Course, School

from authentication.roles import ITManager, Assistant


class IsItManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, ITManager)


class IsAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, Assistant)


class IsITManagerOrIsAssistantForCourse(permissions.BasePermission):

    def has_permission(self, request, view: viewsets):
        is_schools_assistant = True
        if view.action in ["update", "partial_update", "destroy"]:
            course_id = view.kwargs["pk"]
            schools = Course.objects.get(id=course_id).schools.all()

            for school in schools:
                if request.user.user_id != school.assistant.user_id:
                    is_schools_assistant = False
        else:
            school_ids = request.data["schools"]
            for school_id in school_ids:
                school = School.objects.get(id=school_id)
                if request.user.user_id != school.assistant.user_id:
                    is_schools_assistant = False

        return (has_role(request.user.user, ITManager) or
                (has_role(request.user.user, Assistant) and is_schools_assistant))
