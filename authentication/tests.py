from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .factories import StudentUserFactory
from django.urls import reverse_lazy

User = get_user_model()


class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse_lazy("authentication:login")
        user_data = StudentUserFactory.build()
        StudentUserFactory.create(user_id=user_data.user_id, password=user_data.password)
        self.payload = {"user_id": user_data.user_id, "password": user_data.password}

    def test_login_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertTrue(status.is_success(response.status_code))
        self.assertIn("access", response.data)

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
        user_data = StudentUserFactory.build()
        StudentUserFactory.create(user_id=user_data.user_id, password=user_data.password)
        response = self.client.post(reverse_lazy("authentication:login")
                                    , {"user_id": user_data.user_id
                                        , "password": user_data.password})
        self.refresh_token = response.data["refresh"]
        self.access_token = response.data["access"]
        self.payload = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")  # authenticate user

    def test_logout_successful(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_unsuccessful_wrong_refresh_token(self):
        self.payload["refresh"] = "wrong token"
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
