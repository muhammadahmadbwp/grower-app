from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from random import randint
import os

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        user = self.create_user(email, password, **other_fields)
        return user

    def create_user(self, email, password, **other_fields):

        email = self.normalize_email(email)
        user = self.model(**other_fields)
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'surveyor'),
        (3, 'grower'),
    )

    user_name = models.CharField(_('full name'), max_length=100)
    father_name = models.CharField(_('father name'), max_length=100)
    mobile_number = models.CharField(_('mobile number'), max_length=20, unique=True)
    cnic = models.CharField(_('id card number'), max_length=30, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_otp = models.IntegerField(_('activation otp'), default=None, blank=True, null=True)
    notification_token = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email', 'user_name', 'cnic', 'password', 'user_type']


class AdminDetails(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='admin_detail')
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name_address = models.CharField(max_length=250, blank=True, null=True)
    admin_address = models.CharField(max_length=250, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    administration_area = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class SurveyorDetails(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='surveyor_detail')
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name_address = models.CharField(max_length=250, blank=True, null=True)
    surveyor_address = models.CharField(max_length=250, blank=True, null=True)
    circle_name = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class GrowerDetails(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='grower_detail')
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name_address = models.CharField(max_length=250, blank=True, null=True)
    grower_address = models.CharField(max_length=250, blank=True, null=True)
    family_number = models.CharField(max_length=50, blank=True, null=True)
    passbook_number = models.CharField(max_length=50, blank=True, null=True)
    own_land_area = models.IntegerField(blank=True, null=True)
    lease_land_area = models.IntegerField(blank=True, null=True)
    total_land = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)