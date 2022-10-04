from django.core.management import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for i in range(100):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = "@" + self.faker.user_name()
            bio = self.faker.text(500)
            password = self.faker.password()
            email = self.faker.email(first_name,last_name)

            user = User.objects.create_user(username, first_name=first_name,last_name=last_name,email=email,bio = bio, password = password)
            user.save()
