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


class IsITManagerOrIsCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view: viewsets):
        return has_role(request.user, ITManager) or (
                    has_role(request.user, Assistant) and IsCourseAssistant())


class IsCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ["update", "partial_update", "destroy"]:
            is_schools_assistant = self.has_permission_for_update(request, view)
        else:
            is_schools_assistant = self.has_permission_for_create(request)
        return is_schools_assistant

    def has_permission_for_create(self, request):
        school_ids = request.data["schools"]
        for school_id in school_ids:
            school = School.objects.get(id=school_id)
            if request.user.user_id != school.assistant.user_id:
                return False
        return True

    def has_permission_for_update(self, request, view):
        course_id = view.kwargs["pk"]
        schools = Course.objects.get(id=course_id).schools.all()

        for school in schools:
            if request.user.user_id != school.assistant.user_id:
                return False
        return True
