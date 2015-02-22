from django.contrib import admin
# from .models import CPProfile, FBProfile


# @admin.register(CPProfile)
# class CPProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',

#         'user',
#         'first_name',
#         'last_name',
#         'photo',
#         'password_reset_token',
#         'device_id',
#     )


# @admin.register(FBProfile)
# class FBProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',

#         'user',
#         'fb_id',
#         'email',
#         'token',
#     )

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

# def user_unicode(self):
#     return u'{}'.format(self.email)
# User.__unicode__ = user_unicode
