from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from ...models import Employee


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializerClass: This automatically generates fields from the Employee Model, validates the data,
    and creates a user/employee record in the database.
            - class Meta gets the fields of the Model i.e Employee.
            - save method overrides the Model save method, validate email, password, and saves the employee record
            - update method allows for a record to be updated in the database
    """

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'email', 'first_name', 'last_name', 'age', 'password', 'password2')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def save(self, **kwargs):
        user = Employee(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            age=self.validated_data['age']
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Password must match"})

        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(style={'input_type': 'email'}, label=_("Email"))
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Invalid email or password. Try again with correct credentials')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
