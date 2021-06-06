from django.http import request
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile, User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,max_length=68,write_only=True)

    class Meta:
        model = User
        fields = ['email','password','class_name']

    def validate(self, attrs):
        email = attrs.get('email','')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already taken')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(
        min_length=6,max_length=68,write_only=True)
    access = serializers.CharField(max_length=255,read_only=True)
    refresh = serializers.CharField(max_length=255,read_only=True)


    class Meta:
        model = User
        fields = ('email','password','access','refresh')
    
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled,contact admin')
        if not user.status:
            raise AuthenticationFailed('user is inactive,contact admin')

        refresh = RefreshToken.for_user(user)
        return {
            "email":user.email,
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name","last_name","DOB","image"]

    