from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    search_fields = ("username", "email", "first_name", "last_name")

    ordering = ("-date_joined",)

    list_per_page = 25

    readonly_fields = ("last_login", "date_joined")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "joined_at", "display_image")
    list_filter = ("city", "joined_at")
    search_fields = ("user__username", "phone", "city")
    readonly_fields = ("joined_at", "display_image")

    @admin.display(description="Profile Image")
    def display_image(self, obj: Profile) -> str:
        if obj.profile_image:
            return str(
                format_html(
                    '<img src="{}" width="50" height="50" '
                    'style="border-radius:50%;object-fit:cover;">',
                    obj.profile_image.url,
                )
            )
        return "No Image"
