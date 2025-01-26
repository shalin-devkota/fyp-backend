from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserWishlistItem

admin.site.register(CustomUser,UserAdmin)
admin.site.register(UserWishlistItem)