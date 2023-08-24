from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from ...models import Location
# import os
# from ...serializers import CartSerializer
# from django.core import serializers

from django.shortcuts import get_object_or_404
import json
import logging

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class AdminUserCreateAPIList(APIView):

    def get(self,request):
        print("Inside admin get user")
        all_location = Location.objects.all()
        vehicle_choices = CustomUser.VEHICLE_CHOICES

        context = {"all_location" : all_location,
                   "vehicle_choices" : vehicle_choices}

        return render(request, 'admin_add_user.html', context)

class AdminUserAPIList(APIView):
    def get(self, request, user_id=None):
        print("Hear")
        all_location = Location.objects.all()
        vehicle_choices = CustomUser.VEHICLE_CHOICES

        context = {
            "all_location": all_location,
            "vehicle_choices": vehicle_choices
        }

        if user_id is None:
            print("Inside admin get all users")
            user_data = CustomUser.objects.all()
            resulting_list = []
            for user in user_data:
                resulting_dict = {
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'is_verified': user.is_verified,
                    'address': user.address,
                    'otp': user.otp,
                    'is_logged_in': user.is_logged_in,
                    'display_picture': user.display_picture,
                    'vehicle_type': user.vehicle_type,
                    'parking_lot_location': user.parking_lot_location,
                }
                resulting_list.append(resulting_dict)

            context = {"resulting_list" : resulting_list}
            return render(request, 'admin_user_edit.html', context)
        else:
            print(f"Inside admin get single user: {user_id}")
            user = get_object_or_404(CustomUser, id=user_id)
            context["user"] = user
            return render(request, 'admin_user_edit.html', context)



