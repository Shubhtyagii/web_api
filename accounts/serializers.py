from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Employee

from accounts.utils import generate_ref_code

User = get_user_model()
MIN_LENGTH = 8


class User_loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SignUp_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=MIN_LENGTH,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, min_length=MIN_LENGTH, )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'password', 'password2', 'address', 'city',
                  'state', 'zip', 'country', 'referral_code','my_ref_code']

    def validate(self, data):

        if data['password']:
            if data['password'] != data['password2']:
                raise serializers.ValidationError("Password does not match!")
        if data['username']:
            for i in User.objects.all():
                if i.username == data['username']:
                    raise serializers.ValidationError("Username or email is already exists!")
                if i.email == data['email']:
                    raise serializers.ValidationError("email is already exists")
        if data['referral_code']:
            x = User.objects.filter(my_ref_code=data['referral_code'])
            if not x.exists():
                raise serializers.ValidationError("Invalid referral code")

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], email=validated_data['email'],
                                   gender=validated_data['gender'], address=validated_data['address'],
                                   city=validated_data['city'], state=validated_data['state'],
                                   zip=validated_data['zip'], country=validated_data['country'],
                                   referral_code=validated_data['referral_code'])
        user.set_password(validated_data['password'])
        user.save()

        return user



class EmployeeSerializer(serializers.Serializer):
    """
            Employee model serializer
            """
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)


class userdata(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "gender", "address", "city", "state", "zip", "country")
