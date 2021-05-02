from django import forms
from django.core.exceptions import ValidationError
from .models import Employee


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ('email', 'first_name', 'last_name', 'age',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    class Meta:
        model = Employee
        fields = ('email', 'employee_id', 'first_name', 'last_name', 'age', 'is_active', 'is_admin',)
        exclude = ('employee_id',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = Employee.objects.exclude(pk=self.instance.pk).get(email=email)
        except Employee.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % user)
