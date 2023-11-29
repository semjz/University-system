from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from academic.factories import CourseFactory
from academic.serializers import CourseSerializer
from management.factories import FacultyFactory, AssistantFactory
from authentication.factories import (ItManagerUserFactory, StudentUserFactory, ProfessorUserFactory)


class SubjectViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.it_manager_user = ItManagerUserFactory.create()
        self.school = FacultyFactory.create()
        self.assistant = AssistantFactory.create(school=self.school)
        course = CourseFactory.build()
        serializer = CourseSerializer(course)
        self.course_data = serializer.data
        self.course_data["schools"].append(self.school.name)

    def _perform_create_course_request(self, user):
        self.client.force_authenticate(user=user)
        url = reverse("academic:subjects-list")
        response = self.client.post(url, self.course_data, format="json")
        return response

    def _perform_update_course_request(self, user):
        self.client.force_authenticate(user=user)
        payload = {
            "name": "string",
            "credits": 0,
            "type": "general",
            "schools": [
                self.school.name
            ]
        }
        course = CourseFactory.create()
        url = reverse("academic:subjects-detail", kwargs={"pk": course.id})
        response = self.client.patch(url, payload, format="json")
        return response

    def test_create_course_authorized_it_manager(self):
        response = self._perform_create_course_request(self.it_manager_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creat_course_authorized_assistant(self):
        response = self._perform_create_course_request(self.assistant.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_unauthorized_student(self):
        student = StudentUserFactory.create()
        response = self._perform_create_course_request(student)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_unauthorized_professor(self):
        professor = ProfessorUserFactory.create()
        response = self._perform_create_course_request(professor)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_successful_it_manager(self):
        response = self._perform_update_course_request(self.it_manager_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_successful_assistant(self):
        response = self._perform_update_course_request(self.assistant.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_unsuccessful_wrong_assistant(self):
        school = FacultyFactory.create()
        assistant = AssistantFactory.create(school=school)
        response = self._perform_update_course_request(assistant.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
