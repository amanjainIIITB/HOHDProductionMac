from django.test import TestCase, Client
from django.urls import reverse
from customer.views import details, save_mem_visit, save_non_mem_visit, update_mem_client_visit, update_non_mem_client_visit, delete_client_visit
from customer.views import membership, create_membership, update_membership, delete_membership
import json
from useraccount.models import OwnerRegistration, Access
from useraccount.views import signup_view, login_view, logout_view, set_login_session, get_shop_list_access, get_first_shop_id
from useraccount.views import get_page_permission_dict, get_messages
from django.contrib.auth import get_user_model


class TestView(TestCase):

    client = Client() 

    # def setup(self):
    #     login_credentials = {
    #         'phone' : '9999999990',
    #         'Name' : 'Testing',
    #         'password' : 'hohd1234'
    #     }
    #     User = get_user_model()
    #     User.objects.create_user(phone = login_credentials['phone'], password1 = login_credentials['password'], password2 = login_credentials['password'])
    #     logged_in = self.client.login(phone=login_credentials['phone'], password=login_credentials['password'])
    #     session = self.client.session
    #     session['regID'] = 'O1'
    #     session['shop_id'] = 'S1'
    #     session['shop_list_access'] = get_shop_list_access(session['regID'])
    #     session['page_permissions_dict'] = get_page_permission_dict()
    #     session['messages'] = get_messages()
    #     session.save()

    # def test_view_client_visit(self):
    #     url = reverse('details')
    #     response = self.client.get(url, {})

    # def test_create_mem_client_visit(self):
    #     url = reverse('save_mem_visit')
    #     response = self.client.get(url, {})

    # def test_create_non_mem_client_visit_(self):
    #     url = reverse('save_non_mem_visit')
    #     response = self.client.get(url, {})

    # def test_edit_mem_client_visit(self):
    #     url = reverse('update_mem_client_visit')
    #     response = self.client.get(url, {})

    # def test_edit_non_mem_client_visit_(self):
    #     url = reverse('update_non_mem_client_visit')
    #     response = self.client.get(url, {})

    # def test_delete_client_visit(self):
    #     url = reverse('delete_client_visit')
    #     response = self.client.get(url, {})

    # def test_view_membership(self):
    #     self.setup()
    #     # self.client.login(phone='9530101150', password='apc1163@')
    #     response = self.client.get('/client/membership/', follow=True)
    #     print(response)
    #     self.assertEquals(response.status_code, 200)


    # def test_redirects_to_login_page_on_not_loggedin(self):
    #     response = self.client.get(reverse('membership'))
    #     print(response)
    #     self.assertRedirects(response, "/?next=/client/membership/")

    # def test_create_membership(self):
    #     self.setup()
    #     context = {
    #         'custid': 'T1',
    #         'name' : 'Test User',
    #         'contact_number': '9999999990',
    #         'sex': 'male',
    #     }
    #     response = self.client.get('/client/create_membership/', follow=True)
    #     self.assertEquals(response.status_code, 200)

    # def test_edit_membership(self):
    #     url = reverse('update_membership')
    #     response = self.client.get(url, {})

    # def test_delete_membership(self):
    #     url = reverse('delete_membership')
    #     response = self.client.get(url, {})

    # def tearDown(self):
    #     self.client.logout()