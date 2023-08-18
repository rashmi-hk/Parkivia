from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
# import os
from ...serializers import CustomUserSerializer
# from django.core import serializers
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
import concurrent.futures
from django.shortcuts import get_object_or_404
import json
import logging
import secrets
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class StaffVerifyOtpAPIList(APIView):

    def get(self,request):
        print("Inside  get   otp form")
        return render(request, 'staff_otp_verification.html')
        # return render(request, 'new_lohin.html')

    def post(self,request):
        print("Inside otp post", request)
        print("Inside otp up", request.data)
        email = request.data["email"]
        print("email", email)

        entered_otp = request.data["otp"]

        try:
            previous_record = CustomUser.objects.get(email=email)
            print("previous_record", previous_record)
        except ObjectDoesNotExist:
            print("HI")
            # If the user with the specified email does not exist, return a response indicating failure
            response_data = {
                'success': False,
                'message': 'User with this email does not exist.',
            }
            return render(request, 'staff_location.html', context=response_data)

        # verification_status = verify_otp(phone_number, entered_otp)
        # print("verification_status", verification_status)
        print("entered_otp", entered_otp)
        print("previous_record otp", previous_record.otp)
        if entered_otp == previous_record.otp:

            print("verification_status  Updating")
            data_dict = {"is_verified": True}

            serializer = CustomUserSerializer(
                previous_record,
                data=data_dict,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                print("updated", request)
                response_data = {
                    'success': True,
                }
                print("response_data", response_data)
                return redirect('staff_signin')  # Return a JSON response indicating success
            else:
                error_message = 'Error in serializer'
                return render(request, 'staff_otp_verification.html',{'error_message': error_message,'email':email})
        else:
            # If the entered OTP is invalid, return a response indicating failure

            error_message = 'Invalid OTP. Please try again.'
            return render(request, 'staff_otp_verification.html', {'error_message': error_message,'email':email})

