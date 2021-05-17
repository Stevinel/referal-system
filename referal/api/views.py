import random
import string
import time

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import ReferSerializer, UserSerializer


def random_number(size=6, chars=string.ascii_uppercase + string.digits):
    """Generation referal code"""
    return "".join(random.choice(chars) for _ in range(size))


@api_view(["POST"])
def generate_otp(request):
    """Generation sms-code"""
    phone_number = request.data.get("phone_number", None)
    refer_number = random_number()
    if phone_number:
        if User.objects.filter(phone_number=phone_number).exists():
            otp = 5555  # here there should be a random generation of the sms code and sending it
            User.objects.filter(phone_number=phone_number, otp=otp)
            time.sleep(2)
            return Response({"success": True})
        else:
            otp = 5555  # here there should be a random generation of the sms code and sending it
            User.objects.get_or_create(
                phone_number=phone_number,
                otp=otp,
                refer_number=refer_number,
                username=phone_number,
            )
            time.sleep(2)
        return Response({"success": True})
    return Response({"trouble": "ошибка"})


@api_view(["POST"])
def verify_otp(request):
    """SMS confirmation and token receipt"""
    otp = request.data.get("otp", None)
    phone_number = request.data.get("phone_number", None)
    user = User.objects.get(phone_number=phone_number, otp=otp)
    if otp and phone_number:
        try:
            user
        except User.DoesNotExist:
            return Response({"message": "Invalid OTP"})

    token = Token.objects.create(user=user)
    return Response({"token": token.key})


@api_view(["GET", "PUT", "PATCH", "POST"])
@permission_classes([IsAuthenticated])
def profile(request):
    """User profile"""
    if request.method == "GET":
        phone_number = request.data.get("phone_number", None)
        user = User.objects.get(phone_number=phone_number)
        refer_number = user.refer_number
        followers = User.objects.filter(foreign_referal=refer_number)
        serializer = UserSerializer(user)
        serializer_refer = ReferSerializer(followers, many=True)
        if user == request.user:
            return Response(
                {
                    "My profile": serializer.data,
                    "my_refers": serializer_refer.data,
                }
            )
        else:
            return Response(
                {
                    "Profile": serializer.data,
                    "my_refers": serializer_refer.data,
                }
            )
    if request.method == "PUT":
        if request.user.foreign_referal:
            return Response({"You have already entered a referral code"})

        refer_number = request.data.get("refer_number", None)
        try:
            refered_user = User.objects.get(refer_number=refer_number)
        except User.DoesNotExist:
            refered_user = None

        if refered_user is None:
            return Response({"message": "Invalid referal code"})

        serializer = UserSerializer(
            request.user, data={"foreign_referal": refer_number}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
