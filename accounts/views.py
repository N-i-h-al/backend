from rest_framework import status,viewsets
from rest_framework.views import APIView
from .models import UserModel
from .serializers import UserSerializer, LoginSerializer
import random
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta,datetime
from django.conf import settings
from django.utils import timezone

from accounts.utils import send_otp

class UserViewSet(viewsets.ModelViewSet):
    queryset  = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['PATCH'])
    def varify_otp(self,request,pk=None):
        instance = self.get_object()
        if(
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expire
            and timezone.now() < instance.otp_expire
        ):
            instance.is_active = True
            instance.otp_expire = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response(
                "Successfully verified the user.", status=status.HTTP_200_OK
            )
        return Response(
            "User active or Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
            )
    @action(detail=True, methods = ["PATCH"])
    def regenerate_otp(self,request,pk=None):
        instance = self.get_object()
        if int(instance.max_otp_try == 0 and timezone.now() < instance.otp_max_out):
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )
              
        otp = random.randint(1000,9999)
        otp_expire = timezone.now() + timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expire = otp_expire
        instance.max_otp_try = max_otp_try

        if max_otp_try == 0:
            otp_max_out = timezone.now() + timedelta(hours=1)
            instance.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp(instance.phone_number,otp)
        return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)
   


from rest_framework import permissions
from django.contrib.auth import login,logout

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
        context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class LogoutView(APIView):
        def post(self, request):
            request.user.auth_token.delete()
            return Response(status = status.HTTP_200_OK)
