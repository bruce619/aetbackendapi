from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer, AuthCustomTokenSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST',])
@csrf_exempt
@permission_classes([AllowAny])
def create_user(request):
    """
    Create Employee API view.
    :credentials: email, first name, last name, age, password, password2 (comfirm password)
    :param request: Django uses request and response objects to pass state through the system.
    Django creates an HttpRequest object that contains metadata about the request.
    :return:
    """
    if request.method == 'POST':
        data = {}
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered new user"
            data['email'] = user.email
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            token = Token.objects.get(user=user).key
            data["token"] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """
    CustomAuthToken is subclassing the ObtainAuthToken
    Ths class basically lets employees get their token by providing email and password, like a login form.
    """
    serializer_class = AuthCustomTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


obtain_auth_token = CustomAuthToken.as_view()
