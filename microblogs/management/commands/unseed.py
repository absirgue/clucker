from django.core.management import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        fakeUsers = User.objects.all()
        for user in fakeUsers:
            if (user.username != "admin"):
                user.delete()
