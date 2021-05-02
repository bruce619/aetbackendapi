from .serializers import EmployeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from ...models import Employee


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_all_employees(request):
    """
    :param request: Django uses request and response objects to pass state through the system.
    Django creates an HttpRequest object that contains metadata about the request.
    :return: The Function based API returns all employees
    """
    try:
        employee = Employee.objects.all().order_by('join_date')
    except Employee.DoesNotExist as e:
        return Response({'error': e}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee, many=True)
        return Response({'employees': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT', 'PATCH', ])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_update_delete_an_employee(request, employee_id):
    """

    :param request: Django uses request and response objects to pass state through the system.
    Django creates an HttpRequest object that contains metadata about the request.
    :param employee_id: employee ID argument is a string e.g EOOOO1 passed to the URI
    :return: The Function based API returns, update, and delete a specific employee record
    """
    emp_id = employee_id.upper()
    try:
        employee = Employee.objects.get(employee_id=emp_id)
    except Employee.DoesNotExist as e:
        return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response({'employee': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if request.user.is_admin:
            employee.delete()
            return Response({'success': "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': "you do not have the permission to delete this data"},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.user.employee_id != emp_id and not request.user.is_admin:
        return Response({'Response': "You do not have the permission to edit"},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'employee': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'employee': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


