from django.contrib import admin
from .models import User,Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','status','is_active','is_staff','is_superuser','class_name','created_at','updated_at']
    list_filter = ['class_name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','DOB','admin_photo','created_at']
    list_filter = ['user']