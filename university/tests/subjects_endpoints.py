from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from authentication.factories import (ItManagerUserFactory, StudentUserFactory, ProfessorUserFactory)
import university.factories as factories
from ..serializers import CourseSerializer


class SubjectViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.it_manager_user = ItManagerUserFactory.create()
        self.school = factories.SchoolFactory.create()
        self.assistant = factories.AssistantFactory.create(school=self.school)
        course = factories.CourseFactory.build()
        serializer = CourseSerializer(course)
        self.course_data = serializer.data
        self.course_data["schools"].append(self.school.id)

    def _perform_create_course_request(self, user, expected_status):
        self.client.force_authenticate(user=user)
        url = reverse("university:subjects-list")
        response = self.client.post(url, self.course_data, format="json")
        self.assertEqual(response.status_code, expected_status)

    def _perform_update_course_request(self, user, expected_status):
        self.client.force_authenticate(user=user)
        payload = {
            "name": "string",
            "credits": 0,
            "type": "general",
            "schools": [
                self.school.id
            ]
        }
        course = factories.CourseFactory.create()
        url = reverse("university:subjects-detail", kwargs={"pk": course.id})
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, expected_status)

    def test_create_course_authorized_it_manager(self):
        self._perform_create_course_request(self.it_manager_user, status.HTTP_201_CREATED)

    def test_creat_course_authorized_assistant(self):
        self._perform_create_course_request(self.assistant.user, status.HTTP_201_CREATED)

    def test_create_course_unauthorized_student(self):
        student = StudentUserFactory.create()
        self._perform_create_course_request(student, status.HTTP_403_FORBIDDEN)

    def test_create_course_unauthorized_professor(self):
        professor = ProfessorUserFactory.create()
        self._perform_create_course_request(professor, status.HTTP_403_FORBIDDEN)

    def test_update_student_successful_it_manager(self):
        self._perform_update_course_request(self.it_manager_user, status.HTTP_200_OK)

    def test_update_student_successful_assistant(self):
        self._perform_update_course_request(self.assistant.user, status.HTTP_200_OK)
