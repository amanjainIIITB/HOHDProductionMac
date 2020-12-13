from django.test import SimpleTestCase
from django.urls import reverse, resolve
from customer.views import details, save_mem_visit, save_non_mem_visit, update_mem_client_visit, update_non_mem_client_visit, delete_client_visit
from customer.views import membership, create_membership, update_membership, delete_membership

class TestClientVisitUrls(SimpleTestCase):

    def test_client_visit_view_url(self):
        url = reverse('details')
        self.assertEquals(resolve(url).func, details)

    def test_create_membership_client_visit_url(self):
        url = reverse('save_mem_visit')
        self.assertEquals(resolve(url).func, save_mem_visit)

    def test_create_non_membership_client_visit_url(self):
        url = reverse('save_non_mem_visit')
        self.assertEquals(resolve(url).func, save_non_mem_visit)

    def test_edit_membership_client_visit_url(self):
        url = reverse('update_mem_client_visit', args=['visitID'])
        self.assertEquals(resolve(url).func, update_mem_client_visit)

    def test_edit_non_membership_client_visit_url(self):
        url = reverse('update_non_mem_client_visit', args=['visitID'])
        self.assertEquals(resolve(url).func, update_non_mem_client_visit)

    def test_client_visit_delete_url(self):
        url = reverse('delete_client_visit', args=['visitID'])
        self.assertEquals(resolve(url).func, delete_client_visit)


class TestMembershipUrls(SimpleTestCase):

    def test_membership_visit_view_url(self):
        url = reverse('membership')
        self.assertEquals(resolve(url).func, membership)

    def test_create_membership_url(self):
        url = reverse('create_membership')
        self.assertEquals(resolve(url).func, create_membership)

    def test_edit_membership_url(self):
        url = reverse('update_membership', args=['visitID'])
        self.assertEquals(resolve(url).func, update_membership)

    def test_delete_membership_url(self):
        url = reverse('delete_membership', args=['visitID'])
        self.assertEquals(resolve(url).func, delete_membership)