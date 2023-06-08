from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Client, ClientProfile, Staff, StaffProfile, User


class UserAdminConfig(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    search_fields = ('email', 'username', 'first_name', 'last_name')
    filter = ('is_active', 'is_staff')
    ordering = ('-created',)
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_active', 'is_staff'
    )
    readonly_fields = ('updated', )

    # How data is grouped when displaying users
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Stats', {'fields': ('role',)})
    )

    # What fields are displayed when adding users
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
admin.site.register(Client)
admin.site.register(ClientProfile)
