import datetime

from rest_framework import permissions
from rolepermissions.checkers import has_role

from authentication.roles import AssistantRole, StudentRole
from management.models import Faculty, Term
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


class HasTime(permissions.BasePermission):

    def has_permission(self, request, view):
        now_time = datetime.datetime.now()
        end_term_time = Term.objects.get(id=request.data['term']).term_end_time
        end_term_time = datetime.datetime.combine(end_term_time, datetime.datetime.min.time())
        fix_course_end_time = Term.objects.get(id=request.data['term']).fix_course_end_time
        print(end_term_time)
        print(fix_course_end_time)
        return not end_term_time > now_time > fix_course_end_time


class IsAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, AssistantRole)


class IsSameStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return has_role(request.user, StudentRole)

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id
