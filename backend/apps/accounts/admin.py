from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import APIKey, Invitation, Membership, Role, User


@admin.register(User)
class RevantaUserAdmin(UserAdmin):
    list_display = ("email", "display_name", "is_staff")
    ordering = ("email",)


admin.site.register(Role)
admin.site.register(Membership)
admin.site.register(Invitation)
admin.site.register(APIKey)
