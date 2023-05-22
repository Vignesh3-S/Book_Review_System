from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import user,book
from django.contrib.auth.models import Group
from brspro.settings import TEMP_DIR
class AccountAdmin(AdminSite):
    login_template = TEMP_DIR
    model = user
    list_display = ("username","email", "is_staff", "is_active","date_joined","date_modified","last_login")
    list_filter = ("is_superuser",)
    fieldsets = (
        ("Authentication Details", {"fields": ("email","password",)}),
        ("Personal Info",{"fields": ("username","mobilenumber","usertype")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_superuser",)}),
    )
    search_fields = ("email","mobilenumber",)
    ordering = ("email",)


admin.site.register(user)
admin.site.register(book)
admin.site.unregister(Group)