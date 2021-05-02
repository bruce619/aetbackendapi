from rest_framework import serializers
from ...models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
        EmployeeSerializerClass: This automatically generates fields from the Employee Model, validates the data,
        and serializers the data to JSON format.
                - class Meta gets the fields of the Model i.e Employee.
        """

    class Meta:
        model = Employee
        fields = ('employee_id', 'first_name', 'last_name', 'age', 'join_date',)
        read_only_fields = ('employee_id', 'join_date',)
