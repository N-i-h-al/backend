from datetime import timedelta,datetime
from django.conf import settings
import random
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import UserModel
from accounts.utils import send_otp

class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        write_only = True,
        min_length = settings.MAX_PASSWORD_LENGTH,
        error_messages ={
            "min_length" : "Password must be longer than {} charecters".format(
                settings.MAX_PASSWORD_LENGTH
            )
        },
    )
    password2 = serializers.CharField(
        write_only = True,
        min_length = settings.MAX_PASSWORD_LENGTH,
        error_messages ={
            "min_length": "Password must be longer than {} characters".format(
                settings.MAX_PASSWORD_LENGTH
            )
        },
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "password1",
            "password2"
        )
        read_only_fields = ("id",)

    def validate(self,data):
        if(data['password1'] != data['password2']):
            raise serializers.ValidationError("Password do not match")
        return data
    
    def create(self,validated_data):
        otp = random.randint(1000,9999)
        otp_expire = datetime.now() + timedelta(minutes=10)
        user = UserModel(
            phone_number = validated_data['phone_number'],
            email = validated_data['email'],
            otp = otp,
            otp_expire = otp_expire,
            max_otp_try =settings.MAX_OTP_TRY,
        )
        user.set_password(validated_data['password1'])
        account = user.save()
        token = Token.objects.get(user=account).key
        send_otp(validated_data['phone_number'],otp)
        return user
    

from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    
    phone_number = serializers.CharField(
        label="Phone Number",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take phone number and password from request
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "phone number" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs