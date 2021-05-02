from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Employee
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'employee_id', 'first_name', 'last_name', 'age', 'is_admin', 'is_superuser',)
    search_fields = ('email', 'employee_id')
    list_filter = ('is_admin',)
    ordering = ('employee_id',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'age', 'employee_id',)}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'age', 'password1', 'password2'),
        }),
    )


# Now register the new UserAdmin...
admin.site.register(Employee, UserAdmin)
