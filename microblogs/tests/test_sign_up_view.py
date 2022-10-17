"""Tests of the Signup view."""

from django.test import TestCase
from microblogs.forms import SignUpForm
from django.urls import reverse
from microblogs.models import User
from django.contrib.auth.hashers import check_password
from .helper import LogInTester

class SignUpViewTestCase(TestCase,LogInTester):

    def setUp(self):
        # reverse will return the path as it is defined in the URL patern, we do that bcs we are not testing the URL is right here, we are testing the response, test for the URL is another test
        self.url = reverse('sign_up')
        self.form_input = {
        "first_name" : "Jane",
        "last_name" : "Doe",
        "username" : "@janedoe",
        "email" : "janedoe@example.com",
        "bio" : "Hi, I'm Jane.",
        "new_password" : "Password123",
        "password_confirmation" : "Password123",
        }

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_unsuccessful_sign_up(self):
        before_count = User.objects.count()
        self.form_input['username'] = 'BADUSERNAME'
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count +1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')
        user = User.objects.get(username = self.form_input['username'])
        self.assertEqual(user.first_name, self.form_input['first_name'])
        self.assertEqual(user.last_name, self.form_input['last_name'])
        self.assertEqual(user.email, self.form_input['email'])
        self.assertEqual(user.bio, self.form_input['bio'])
        is_password_correct = check_password(self.form_input['new_password'],user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
