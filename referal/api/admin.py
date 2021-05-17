from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "refer_number", "otp", "foreign_referal")
    empty_value_display = "-пусто-"
