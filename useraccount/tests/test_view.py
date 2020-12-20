from django.test import TestCase, Client
from django.urls import reverse
from useraccount.views import signup_view, login_post, logout_view
from staff.views import shopreg, aboutus
import json

class TestView(TestCase):
    client = Client()
    
    def test_login_view(self):

        # Sign up as a Client
        url = reverse('signup_view')
        print(url)
        response = self.client.post(url, {
            'Name' : 'automation_test',
            'phone': '9530101155',
            'password1': 'apc1163@',
            'password2': 'apc1163@'
        })


        # Sign up for Partner
        url = reverse('signup_view')
        print(url)
        response = self.client.post(url, {
            'Name' : 'Create Partner',
            'phone': '9530101156',
            'password1': 'apc1163@',
            'password2': 'apc1163@'
        })


        # Login as a client
        url = reverse('login_post')
        credentials = {
            'phone': '9530101155',
            'password': 'apc1163@'
        } 
        response = self.client.post(url, credentials)


        # # GET, About us
        url = '/staff/aboutus/'
        response = self.client.get(url)


        # # GET, Shop Registration
        url = '/staff/shopreg/'
        response = self.client.get(url)

    
        # POST, Shop Registration
        url = '/staff/shopreg/'
        data = {
            'Shop_Name': 'Test',
            'Desk_Contact_Number': '1234567890',
            'email' : 'test@gmail.com',
            'Shop_Address' : 'Head Office at Bellandur, Bangalore'
        }
        response = self.client.post(url, data)


        # Get, Add Partner 
        url = '/staff/add_partner/'
        response = self.client.get(url)


        # POST, Add Partner
        url = '/staff/add_partner/'
        data = {
            'contact_number' : '9530101156',
            'shop_list[]' : list('O1')
        }
        response = self.client.post(url, data)

        # Get, membership
        url = '/client/membership/'
        response = self.client.get(url)


        # POST, create_membership

        # Edit, membership

        # Get, client
        url = '/client/details/'
        response = self.client.get(url)


        # POST, Visit membership Client

        # Edit, Visit membership Client

        # POST, Visit Non-membership Client 

        # Edit, Visit Non-membership client

        # Get, Appointment
        url = '/staff/appointment/'
        response = self.client.get(url)

        # POST, create Appointment for membership client

        # POST, create Appointment for non-membership client

        # DELETE, client visit

        # Delete, membership