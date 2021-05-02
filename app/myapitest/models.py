from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager
from django.utils import timezone


def ids():
    no = Employee.objects.count()
    if no is None:
        return 1
    else:
        return no + 1


class Employee(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', unique=True, error_messages={
        'unique': "A user with that email already exists.",
    })
    employee_id = models.CharField(verbose_name="Employee ID", max_length=6, unique=True, error_messages={
        'unique': "A employee id already exists.",
    })
    first_name = models.CharField(verbose_name='First Name', max_length=30)
    last_name = models.CharField(verbose_name='Last Name', max_length=30)
    age = models.CharField(verbose_name="Age", max_length=3)
    join_date = models.DateTimeField(verbose_name='Date Joined', default=timezone.now)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

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
            self.employee_id = "E%05d" % ids()
        super(Employee, self).save(*args, **kwargs)

