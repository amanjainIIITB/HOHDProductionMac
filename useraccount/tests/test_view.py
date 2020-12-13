from django.test import TestCase, Client
from django.urls import reverse
from useraccount.views import signup_view, login_view, logout_view
import json

class TestView(TestCase):

    # def test_signup_view(self):
    #     url = reverse('signup_view')
    #     print(url)
    #     response = Client().post(url, {
    #         'Name' : 'automation_test',
    #         'phone': '9530101155',
    #         'password1': 'apc1163@',
    #         'password2': 'apc1163@'
    #     })
    #     print(response)
    #     self.assertEquals(response.status_code, 200)

    def test_login_view(self):
        client = Client()
        client.login(phone='9530101150', password='apc1163@')
        url = reverse('login_view')
        credentials = {
            'phone': '9530101150',
            'password': 'apc1163@'
        }
        response = Client().post(url, credentials)
        print()
        print()
        print('Hello')
        print()
        print()
        print(response)
        # return client
        self.assertEquals(response.status_code, 200)