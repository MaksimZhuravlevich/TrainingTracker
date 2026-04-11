from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'user_age', 'user_weight', 'user_height']
    list_filter = ['is_staff', 'is_superuser', 'male']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'male', 'user_age', 'user_weight', 'user_height')
        }),
        ('Адрес', {
            'fields': ('address1', 'address2', 'city', 'country', 'province', 'postal_code', 'phone')
        }),
        ('Маркетинг', {
            'fields': ('marketing_consent1', 'marketing_consent2')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'male', 'user_age', 'user_weight',
                       'user_height'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)