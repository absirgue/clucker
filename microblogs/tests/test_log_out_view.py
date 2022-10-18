"""Tests of the log form_input  view."""

from django.test import TestCase
from django.urls import reverse
from microblogs.models import User
from .helper import LogInTester

class LogOutViewTestCase(TestCase,LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user('@johndoe', first_name="John", last_name= "Doe", email="jdoe@example.com", bio="Hi I'm John!", password='Password123', is_active=True)

    def test_get_log_out(self):
        self.client.login(username = '@johndoe', password = 'Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow = True)
        # We want logging out to send back to home page
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,'home.html')
        self.assertFalse(self._is_logged_in())


    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')
