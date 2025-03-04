from django.contrib import admin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_active'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ('user',)
    # search_fields = ('user__email', 'bio')
    # ordering = ('user__email',)
    # list_filter = ('user__is_staff', 'user__is_superuser')
    pass
