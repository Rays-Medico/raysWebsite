from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'address')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_birth', 'address', 'age')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_birth', 'address', 'age')}),
    )

# Register your custom User model with the custom admin
admin.site.register(User, CustomUserAdmin)