""" Configuration of the admin interface for microblogs """

from django.contrib import admin
from .models import User

# This is a decorator to register the model class we wish to administer with this admin class
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""
    # list_display lists the attributes we want to see n the display of the User db records
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active']
