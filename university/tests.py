from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Term
import random
import string


User = get_user_model()

fake = Faker(["fa_IR"])
roles = ["student", "professor", "assistant"]
genders = ["male", "female"]
password = fake.password()
user_id = ''.join(random.choice(string.digits) for _ in range(4))


class TermAPITestCase(APITestCase):
    def setUp(self):
        self.registered_user = baker.prepare(User, user_id=user_id, password=password)
        self.registered_user.set_password(password)
        self.registered_user.save()
        self.term_instance = baker.prepare('university.Term')
        response = self.client.post(reverse_lazy("authentication:login"),
                                    {"user_id": self.registered_user.user_id, "password": password})
        self.refresh_token = response.data["refresh"]
        self.access_token = response.data["access"]
        self.payload = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_term(self):
        term_data = {
            "year": 1400,
            "term_type": "bahman",
        }
        response = self.client.post('/admin/term/', term_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Term.objects.filter(year=1400, term_type="bahman").exists())

    def test_list_terms(self):
        self.client.force_authenticate(user=self.payload)
        response = self.client.get('/admin/term/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Term.objects.count())

    def test_retrieve_term(self):
        self.client.force_authenticate(user=self.payload)
        response = self.client.get(f'/admin/term/{self.term.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['year'], self.term.year)
        self.assertEqual(response.data['term_type'], self.term.term_type)

    def test_update_term(self):
        self.client.force_authenticate(user=self.payload)
        updated_data = {
            "year": 1400,
            "term_type": "bahman",
            # دیگر فیلدها را با مقادیر مناسب پر کنید
        }
        response = self.client.put(f'/admin/term/{self.term.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.term.refresh_from_db()
        self.assertEqual(self.term.year, updated_data['year'])
        self.assertEqual(self.term.term_type, updated_data['term_type'])

    def test_delete_term(self):
        self.client.force_authenticate(user=self.payload)
        response = self.client.delete(f'/admin/term/{self.term.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Term.objects.filter(id=self.term.id).exists())
