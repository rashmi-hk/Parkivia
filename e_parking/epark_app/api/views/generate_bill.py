from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser,SlotBooking
from ...serializers import CustomUserSerializer
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from ...models import Location
from rest_framework import status

from django.shortcuts import get_object_or_404
import json
import logging

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class GenerateBillFormAPIList(APIView):

    def get(self,request):
        print("Inside GenerateBillFormAPIList",request)
        print("Inside GenerateBillFormAPIList",request.data)

        booking_id = request.GET.get('booking_id')
        vehicle_number = request.GET.get('vehicle_number')

        book_obj = SlotBooking.objects.get(id=booking_id)

        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)



        context = {"slot" : book_obj.slot,
                   "check_in_time" : book_obj.check_in_time,
                   "vehicle_number" : book_obj.vehicle_number,
                   "vehicle_type" : book_obj.vehicle_type,
                   "amount" : book_obj.amount,
                   "check_out_time" : book_obj.check_out_time}
        print("context", context)
        if user.is_superuser:
            print("super user")
            return render(request, 'admin_generate_bill.html', context)
        else:
            print("Not super user")
            return render(request, 'staff_generate_bill.html', context)


