from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'role', 'is_staff')
    list_filter = ('is_staff', 'username')
    fieldsets = (
        ('ФИО', {'fields': ('username',)}),
        ('Персональная информация', {'fields': ('role',)}),
        ('Разрешения', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('firstname', 'secondname', 'role', 'is_staff', 'password1', 'password2')}
         ),
    )
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
