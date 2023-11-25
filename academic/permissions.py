from rest_framework import permissions, viewsets
from rolepermissions.checkers import has_role

from authentication.roles import ITManager, Assistant
from management.models import Faculty
from academic.models import Course


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
            school = Faculty.objects.get(id=school_id)
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


class IsITManagerOrIsCourseAssistant(permissions.BasePermission):

    def has_permission(self, request, view: viewsets):
        return has_role(request.user, ITManager) or (
                has_role(request.user, Assistant) and IsCourseAssistant())