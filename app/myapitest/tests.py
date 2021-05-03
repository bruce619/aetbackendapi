from .models import Employee
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def register_employee(self):
        data = {
            "email": "test@gamil.com", "first_name": "Test",
            "last_name": "Boss", "age": "30",
            "password": "strongpassword", "password2": "strongpassword"
        }
        res = self.client.post('/api/create-user', data)
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)


class ObtainApiTokenTestCase(APITestCase):

    def setUp(self):
        self.user = Employee.objects.create_user(email="david@gmail.com", password="izanami")
        self.token = Token.objects.create(user=self.user)

    def obtain_token(self):
        data = {
            "email": "david@gmail.com",
            "password": "izanami"
        }
        res = self.client.post('/api/user/token', data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["token"], self.token.key)
