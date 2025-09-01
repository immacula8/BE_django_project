from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscription, Comment

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # show fields in the admin list
    list_display = ["username", "email", "is_staff", "is_active", "date_of_birth", "subscription_plan"]
    # fields for editing
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo", "subscription_plan")}),
    )
    # fields when creating new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)
admin.site.register(Comment)

