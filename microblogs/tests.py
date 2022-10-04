from django.test import TestCase
from .models import User
from django.core.exceptions import ValidationError

class UserModelTestCase(TestCase):
    #setup runs before each test, needs to have exact same signature.
    def setUp(self):
        self.user = User.objects.create_user(
        "@johndoe",
        first_name = "John",
        last_name = "Doe",
        email = "jdoe@example.org",
        password="password123",
        bio="Hey, I'm John :)"
        )

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x'*29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x'*32
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        user = User.objects.create_user(
        "@janedoe",
        first_name = "Jane",
        last_name = "Doe",
        email = "janedoe@example.org",
        password="password123",
        bio="Hey, I'm Jane :)"
        )
        self.user.username = "@janedoe"
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphaneumerical_after_that(self):
        self.user.username = "@john!doe"
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_three_alphaneumerical_after_that(self):
        self.user.username = "@jo"
        self._assert_user_is_invalid()

    def test_username_contain_numbers(self):
        self.user.username = "@j3o"
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = "@@johndoe"
        self._assert_user_is_invalid()

    def test_first_name_can_not_be_blank(self):
        self.user.first_name = ""
        self._assert_user_is_invalid()

    def test_first_name_can_be_repeated(self):
        user = User.objects.create_user(
        "@janedoe",
        first_name = "Jane",
        last_name = "Doe",
        email = "janedoe@example.org",
        password="password123",
        bio="Hey, I'm Jane :)"
        )
        self.user.first_name = "Jane"
        self._assert_user_is_valid()

    def test_first_name_can_have_fifty_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_can_not_be_over_fifty_character(self):
        self.user.first_name = 'x'*51
        self._assert_user_is_invalid()

    def test_last_name_can_not_be_blank(self):
        self.user.last_name = ""
        self._assert_user_is_invalid()

    def test_last_name_can_be_repeated(self):
        user = User.objects.create_user(
        "@janedoe",
        first_name = "Jane",
        last_name = "Doe",
        email = "janedoe@example.org",
        password="password123",
        bio="Hey, I'm Jane :)"
        )
        self.user.last_name = "Jane"
        self._assert_user_is_valid()

    def test_last_name_can_have_fifty_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_can_not_be_over_fifty_character(self):
        self.user.last_name = 'x'*51

    def test_email_must_be_unique(self):
        user = User.objects.create_user(
        "@janedoe",
        first_name = "Jane",
        last_name = "Doe",
        email = "janedoe@example.org",
        password="password123",
        bio="Hey, I'm Jane :)"
        )
        self.user.email = "janedoe@example.org"
        self._assert_user_is_invalid()

    def test_email_must_have_at(self):
        self.user.email = "helloworld.com"
        self._assert_user_is_invalid()

    def test_email_must_have_dot(self):
        self.user.email = "hello@world"
        self._assert_user_is_invalid()

    def test_email_must_have_at_before_dot(self):
        self.user.email = "hello.world@hi"
        self._assert_user_is_invalid

    def test_valid_email_is_accepted(self):
        self._assert_user_is_valid()

    def test_email_must_have_domain(self):
        self.user.email = "john@.com"
        self._assert_user_is_invalid()

    def test_email_can_not_have_two_at(self):
        self.user.email = "john@@hello.com"
        self._assert_user_is_invalid()

    def test_email_must_have_username(self):
        self.user.email = "@hello.com"
        self._assert_user_is_invalid()

    def test_bio_can_not_be_over_520_characters(self):
        self.user.bio = 'x' *521
        self._assert_user_is_invalid()

    def test_bio_can_be_520_characters(self):
        self.user.bio = 'x' *520
        self._assert_user_is_valid()

    def test_bio_can_be_blank(self):
        self.user.bio = ""
        self._assert_user_is_valid()

    def test_bio_may_already_exist(self):
        user = User.objects.create_user(
        "@janedoe",
        first_name = "Jane",
        last_name = "Doe",
        email = "janedoe@example.org",
        password="password123",
        bio="Hey, I'm Jane :)"
        )
        self.user.bio = "Hey, I'm Jane :)"
        self._assert_user_is_valid()

    def _assert_user_is_valid(self):
        try:
            #The full_clean throws a ValidationError if user is not valid.
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid.")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
