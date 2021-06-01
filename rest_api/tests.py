from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_api.tools import get_object_or_none


class AccountTests(APITestCase):
    users_length = 7
    def setUp(self):
        # Set up data for the whole TestCase
        for i in range(self.users_length):
            User.objects.create(username="admin_{}".format(i), password='admin')
    def test_get_all_users_with_size(self):
        """
        Ensure we can create a new account object.
        """
        self.client.login(username='ruslan', password='gorod116')
        url = reverse('rest_api-users')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if self.users_length < 10:
            self.assertEqual(len(response.data), self.users_length)
        else:
            self.assertEqual(len(response.data), 10)

    def test_user_detail_put(self):
        url = reverse('rest_api-user_detail', kwargs={'id':1})
        user = get_object_or_none(User, id=1)
        response = self.client.put(url, {"email": "731ruslan@mail.ru", 'first_name': 'ruslan'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)