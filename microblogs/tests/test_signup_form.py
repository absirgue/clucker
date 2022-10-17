from django.test import TestCase
from microblogs.models import User
from microblogs.forms import SignUpForm
from django import forms
from django.contrib.auth.hashers import check_password

""" Good practice to first list what we have to test. As such:
- form acceptsa valid inputs data
- form has the necessary fields
- form users model Validation
- new password has a correct format (the form takes care of this validation properly)
- new password and password confirmation are the same
"""
class SignUpFormTestCase(TestCase):
    """Unit tests for the sign up form"""

    def setUp(self):
        self.form_input = {
        "first_name" : "Jane",
        "last_name" : "Doe",
        "username" : "@janedoe",
        "email" : "janedoe@example.com",
        "bio" : "Hi, I'm Jane.",
        "new_password" : "Password123",
        "password_confirmation" : "Password123",
        }

    # Form acceptsa valid inputs data
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Form has the necessary fields
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn("bio", form.fields)
        self.assertIn("new_password", form.fields)
        new_pwd_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_pwd_widget, forms.PasswordInput))
        self.assertIn("password_confirmation", form.fields)
        pwd_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(pwd_confirmation_widget, forms.PasswordInput))

    # Form users model Validation
    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # New password has a correct format (we want each password to contain at least an upper case character, a lower case chracter, and a number)
    def test_password_must_contain_upper_case_character(self):
        self.form_input['new_password'] = 'badpwd123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lower_case_character(self):
        self.form_input['new_password'] = 'BADPWD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'BaDpWd'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # New password matches password confirmation
    def test_password_macthes_confirmation(self):
        self.form_input['password_confirmation'] = 'BaDpWd'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count,before_count + 1)
        user = User.objects.get(username = "@janedoe")
        self.assertEqual(user.first_name,"Jane")
        self.assertEqual(user.last_name,"Doe")
        self.assertEqual(user.email,"janedoe@example.com")
        self.assertEqual(user.bio,"Hi, I'm Jane.")
        self.assertTrue(check_password("Password123",user.password))
