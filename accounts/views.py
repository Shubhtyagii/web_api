from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import Employee
from accounts.serializers import SignUp_Serializer, EmployeeSerializer, User_loginSerializer
from accounts.utils import get_tokens_for_user

User = get_user_model()
from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    response = Response()
    # user = authenticate(email=email,password=password)
    # print(user,'///')
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'email and password required')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('user not found')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    token = get_tokens_for_user(user)
    # print(token['access'])
    serialized_user = User_loginSerializer(user)
    response.data = {
        'access_token': token['access'],
        'refresh_token': token['refresh'],
        'user': serialized_user.data,
    }

    return response


@authentication_classes([SessionAuthentication, JWTAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Employee_api(request):
    if request.method == "GET":
        emp = Employee.objects.all()
        serializer = EmployeeSerializer(emp, many=True)
        # print(serializer)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = EmployeeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'record added'})
        return Response(serializer.errors)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUp_Serializer
