from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, CustomerProfile, Staff, StaffProfile, User


class UserAdminConfig(UserAdmin):

    search_fields = ('email', 'username', 'first_name', 'last_name')
    filter = ('is_active', 'is_staff')
    ordering = ('-created',)
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_active', 'is_staff'
    )

    # How data is grouped when displayed
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Stats', {'fields': ('role',)})
    )

    # What fields are displayed when adding records
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'email', 'password1',
                'password2'
            )
        }),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Staff)
admin.site.register(StaffProfile)
admin.site.register(Customer)
admin.site.register(CustomerProfile)
