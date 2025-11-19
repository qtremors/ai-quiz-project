from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {'fields': ('is_student', 'avatar')}),
    )

admin.site.register(User, CustomUserAdmin)