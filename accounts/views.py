from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Employee
from accounts.serializers import SignUp_Serializer, EmployeeSerializer

User = get_user_model()
from rest_framework import viewsets


@authentication_classes([SessionAuthentication,JWTAuthentication])
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Employee_api(request, pk=None):
    if request.method == "GET":
        id = pk
        if id is not None:
            try:
                emp = Employee.objects.get(id=id)
                serializer = EmployeeSerializer(emp)

                return Response(serializer.data)
            except:
                return Response({'msg': 'id does not exists'})

        emp = Employee.objects.all()
        serializer = EmployeeSerializer(emp, many=True)
        print(serializer)
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
