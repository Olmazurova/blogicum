from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserBlogicum


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('info', 'birthday',)}),
)

admin.site.register(UserBlogicum, UserAdmin)
