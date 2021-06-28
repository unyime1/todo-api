from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

UserModel = get_user_model()
from .models import *


class CreateUserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def validate_password(self, value):
        #validate password length
        if len(value) < 8:
            raise serializers.ValidationError("PASSWORD_TOO_SHORT")
        return value

    def validate_email(self, value):
        #validate email
        #convert submitted emmail to lowercase
        lower_case_email = value.lower()
        #check if email exists in user table
        user_email = UserModel.objects.filter(email=lower_case_email)
        if user_email:
            raise serializers.ValidationError("EMAIL_EXISTS")
        return value

    def create(self, validated_data):
        #convert the email to lowercase
        lower_case_email = validated_data['email'].lower()
        #create user
      
        user = UserModel.objects.create(
            email=lower_case_email,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = (
            'username', 'password', 'email', 'first_name',
            'last_name'
        )
        write_only_fields = ('password',)



class LoginSerializer(serializers.Serializer):
    """This serializer handles user login"""
    email = serializers.EmailField()
    password = serializers.CharField(style = {'input_type' : 'password' }, trim_whitespace = False)

    def validate_email(self, value):
        #validate email to return only lowercased values
        return value.lower()

    def validate(self, attrs):
        #validate and authenticate users
        #convert entered emails to lowercase and authenticate user
        email = attrs.get('email')
        password = attrs.get('password')

        #authenticate users
        user = authenticate(request = self.context.get('request'), username = email, password = password)

        if not user:
            raise serializers.ValidationError("CREDENTIALS_INCORRECT")

        attrs['user'] = user
        return attrs 
