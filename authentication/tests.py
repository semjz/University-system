from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from faker import Faker
import random
import string
from django.urls import reverse_lazy

User = get_user_model()
fake = Faker(["fa_IR"])
roles = ["student", "professor", "assistant"]
genders = ["male", "female"]
password = fake.password()
user_id = ''.join(random.choice(string.digits) for _ in range(4))


class RegisterTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse_lazy("authentication:register")

        self.existing_user = baker.make(User)
        self.existing_user_national_code = self.existing_user.national_code
        self.payload = {"first_name": fake.first_name(), "last_name": fake.last_name()
                         , "national_code": f"0{fake.passport_number()}", "phone_number": "09120000001"
                         , "email": fake.email(), "role": random.choice(roles)
                         , "gender": random.choice(genders), "password": password
                         , "confirm_password": password}

    def test_register_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertTrue(status.is_success(response.status_code))

    def test_register_unsuccessful_duplicate_national_code(self):
        self.payload["national_code"] = self.existing_user_national_code
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy("authentication:login")
        self.registered_user = baker.prepare(User, user_id=user_id, password=password)
        self.registered_user.set_password(password)
        self.registered_user.save()
        self.payload = {"user_id": self.registered_user.user_id, "password": password}

    def test_login_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIn('access', response.data)

    def test_login_unsuccessful_wrong_password(self):
        self.payload["password"] = "wrong password"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)

    def test_login_unsuccessful_wrong_user_id(self):
        self.payload["user_id"] = "-1111"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)


class LogoutTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy("authentication:logout")
        self.registered_user = baker.prepare(User, user_id=user_id, password=password)
        self.registered_user.set_password(password)
        self.registered_user.save()
        response = self.client.post(reverse_lazy("authentication:login")
                                    , {"user_id": self.registered_user.user_id, "password": password})
        self.refresh_token = response.data["refresh"]
        self.access_token = response.data["access"]
        self.payload = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}") # authenticate user

    def test_logout_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_unsuccessful_wrong_refresh_token(self):
        self.payload["refresh"] = "wrong token"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
