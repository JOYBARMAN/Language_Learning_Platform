from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User, Profile, UserOtp
from core.forms import UserCreationForm


class ProfileInline(admin.StackedInline):
    """
    Inline for the Profile model to manage it directly within the User admin.
    """

    model = Profile
    extra = 0
    can_delete = False
    readonly_fields = ("latitude", "longitude")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["uid", "email", "last_login"]
    fieldsets = (
        (None, {"fields": ("email", "password", "new_password")}),
        (
            "Other",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "uid",
                    "last_login",
                    "status",
                    "user_type",
                )
            },
        ),
        (
            "User Permission",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    list_filter = [
        "is_superuser",
        "is_staff",
        "status",
        "last_login",
    ]
    search_fields = ("phone", "email")
    readonly_fields = ("password", "uid", "last_login")
    list_select_related = True
    show_full_result_count = False
    form = UserCreationForm
    inlines = [ProfileInline]
    ordering = ("-created_at",)

    filter_horizontal = ("groups", "user_permissions")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "full_name",
        "user_email",
        "user_phone",
        "gender",
        "blood_group",
    )
    search_fields = ("user__email",)

    def user_name(self, obj):
        return f"{obj.user.get_username()}"

    user_name.short_description = "Username"  # Set a custom column header

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"  # Set a custom column header

    def user_phone(self, obj):
        return obj.user.phone

    user_phone.short_description = "Phone"


# User otp model admin site
@admin.register(UserOtp)
class UserOtpAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "otp_type",
        "otp",
        "is_activated",
    )
    search_fields = ("user__email",)

    def user_name(self, obj):
        return f"{obj.user.get_username()}"

    user_name.short_description = "Username"
