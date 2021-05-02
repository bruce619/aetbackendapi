from django.urls import path
from .views import (
    get_all_employees,
    get_update_delete_an_employee
)

urlpatterns = [
    path('employees', get_all_employees, name="employees"),
    path('employee/<str:employee_id>', get_update_delete_an_employee, name="employee")
]