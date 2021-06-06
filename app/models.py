from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin,BaseUserManager )
from django.utils.safestring import mark_safe

class UserManager(BaseUserManager):
    def create_user(self,email,class_name,password=None,):
        if not email:
            raise TypeError("Email Required")
        user = self.model(email=self.normalize_email(email),class_name=class_name)
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self,email,password=None):
        if not password:
            raise TypeError("Password should not be none")
        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class_name = (
    ('8th','8th'),
    ('9th','9th'),
    ('10th','10th')
)
class User(AbstractBaseUser,PermissionsMixin):
    id          = models.AutoField(primary_key=True)
    email       = models.CharField(max_length=255,unique=True,db_index=True)
    status      = models.BooleanField(default=False)
    class_name  = models.CharField(max_length=20,choices=class_name)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['class_name']

    def __str__(self):
        return self.email

class Profile(models.Model):
    id         = models.AutoField(primary_key=True)
    user       = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    DOB        = models.DateField()
    image      = models.ImageField(upload_to='profiles/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name +" "+self.last_name

    def admin_photo(self):
        return mark_safe('<img src="{}" width="70 />'.format(self.image.url))
    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True