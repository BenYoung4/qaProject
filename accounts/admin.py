from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'is_customer',
                    'is_helpdesk'
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
