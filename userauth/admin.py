from django.contrib import admin
from .models import User, Contact, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'bio', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Profile)