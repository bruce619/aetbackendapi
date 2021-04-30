from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True, null=False, blank=False, error_messages={
        'unique': "A user with that email already exists.",
    })
    employee_id = models.CharField(verbose_name="Employee ID", unique=True)
    first_name = models.CharField(verbose_name='First Name', max_length=30)
    last_name = models.CharField(verbose_name='Last Name', max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)
    join_date = models.DateTimeField(verbose_name='Date Joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = "E%05d" % self.pk
        super().save(**kwargs)


