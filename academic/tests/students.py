from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from management.factories import AssistantFactory, StudentFactory, MajorFactory, FacultyFactory
from academic.serializers import StudentUpdateStudentSerializer, AssistantUpdateStudentSerializer


class StudentViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.assistant = AssistantFactory.create()
        self.student1 = StudentFactory.create()
        self.student2 = StudentFactory.create()
        student = StudentFactory.build(major=MajorFactory.create(), school=FacultyFactory.create())
        self.assistant_student_payload = AssistantUpdateStudentSerializer(student).data
        self.student_student_payload = StudentUpdateStudentSerializer(student).data

    def _perform_retrieve_student_request(self, user, student):
        self.client.force_authenticate(user=user)
        url = reverse("academic:students-detail", kwargs={"pk": student.user_id})
        return self.client.get(path=url)

    def _perform_list_student_request(self, user):
        self.client.force_authenticate(user=user)
        url = reverse("academic:students-list")
        return self.client.get(path=url)

    def _perform_update_student_request(self, user, payload):
        self.client.force_authenticate(user=user)
        url = reverse("academic:students-detail", kwargs={"pk": self.student1.user_id})
        return self.client.put(path=url, data=payload, format='json')

    def test_retrieve_student_by_assistant_successful(self):
        response = self._perform_retrieve_student_request(self.assistant.user, self.student1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_student_by_student_successful(self):
        response = self._perform_retrieve_student_request(self.student1.user, self.student1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_student_by_wrong_student_unsuccessful(self):
        response = self._perform_retrieve_student_request(self.student1.user, self.student2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_student_by_assistant_successful(self):
        response = self._perform_list_student_request(self.assistant.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_student_by_student_unsuccessful(self):
        response = self._perform_list_student_request(self.student1.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_by_assistant_successful(self):
        response = self._perform_update_student_request(self.assistant.user
                                                        , self.assistant_student_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_by_student_successful(self):
        response = self._perform_update_student_request(self.student1.user
                                                        , self.student_student_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_by_student_modify_user_id_unsuccessful(self):
        response = self._perform_update_student_request(self.student1.user
                                                        , self.assistant_student_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
