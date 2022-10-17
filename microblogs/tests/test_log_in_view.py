"""Tests of the log in  view."""

from django.test import TestCase
from microblogs.forms import LogInForm
from django.urls import reverse
from microblogs.models import User
from .helper import LogInTester

class LogInViewTestCase(TestCase,LogInTester):

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user('@johndoe', first_name="John", last_name= "Doe", email="jdoe@example.com", bio="Hi I'm John!", password='Password123', is_active=True)
        self.form_input = {
        "username" : "@janedoe",
        "password" : "Password123",
        }

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_unsuccessful_log_in(self):
        form_input = {
        "username" : "@janedoe",
        "password" : "Password123",
        }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        # In an unsuccessful log in screen, we want the form to not be bound so the user has to enter from scratch again
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {
        "username" : "@johndoe",
        "password" : "Password123",
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')

    def test_valid_log_in_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {
        "username" : "@johndoe",
        "password" : "Password123",
        }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('feed')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        # In an unsuccessful log in screen, we want the form to not be bound so the user has to enter from scratch again
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
