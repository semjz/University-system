from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import StudentFactory, MajorFactory, SchoolFactory
from authentication.factories import (ItManagerUserFactory, StudentUserFactory, AssistantUserFactory
, ProfessorUserFactory)
from ..models import Student
from ..serializers import CreateStudentSerializer


class ITManagerStudentViewSet(APITestCase):
    def setUp(self) -> None:
        self.user_it_manager = ItManagerUserFactory.create(last_name="random1")
        self.user_student = StudentUserFactory.create(last_name="random2")
        self.user_professor = ProfessorUserFactory.create(last_name="random3")
        self.user_assistant = AssistantUserFactory.create(last_name="random4")
        major = MajorFactory.create()
        school = SchoolFactory.create()
        student = StudentFactory.build(school=school, major=major)
        serializer = CreateStudentSerializer(student)
        self.student_data = serializer.data
        self.student_data["user"]["confirm_password"] = student.user.password

    def _perform_create_student_request(self, user, expected_status, num_of_students):
        self.client.force_authenticate(user=user)
        url = reverse("university:admin-student-list")
        response = self.client.post(url, self.student_data, format="json")
        students = Student.objects.all()
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(len(students), num_of_students)

    def test_create_student_authorized(self):
        self._perform_create_student_request(self.user_it_manager, status.HTTP_201_CREATED, 1)

    def test_create_student_not_authorized_student(self):
        self._perform_create_student_request(self.user_student, status.HTTP_403_FORBIDDEN, 0)

    def test_create_student_not_authorized_professor(self):
        self._perform_create_student_request(self.user_professor, status.HTTP_403_FORBIDDEN, 0)

    def test_create_student_not_authorized_assistant(self):
        self._perform_create_student_request(self.user_assistant, status.HTTP_403_FORBIDDEN, 0)

    def test_update_student_successful(self):
        self.client.force_authenticate(user=self.user_it_manager)
        payload = {
            "user": {
                "first_name": "Update name"
            },
            "entrance_year": 3000
        }
        student = StudentFactory.create()
        url = reverse("university:admin-student-detail", kwargs={"pk": student.user_id})
        response = self.client.patch(url, payload, format="json")
        self.assertTrue(status.is_success(response.status_code))


