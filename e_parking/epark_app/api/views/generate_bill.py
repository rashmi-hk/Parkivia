from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser,SlotBooking,SlotDetail,SlotDetailVariant
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
        slot_id = request.GET.get('slot_id')
        vehical_type = request.GET.get('vehical_type')
        print("vehicle_type", vehical_type)
        print("vehicle_type", type(vehical_type))
        booking_id = request.GET.get('booking_id')


        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)
        book_obj = SlotBooking.objects.get(id=booking_id)
        book_obj.is_bill_generated = True
        book_obj.save()

        slot_obj = SlotDetail.objects.get(id=slot_id)
        print("slot_obj", slot_obj)
        variants = SlotDetailVariant.objects.filter(slot=slot_obj, vehicle_type=vehical_type)
        print("variants", variants)
        # Iterate through the variants and update available_slots
        for variant in variants:
            print("Inside for incresed ***********************")
            variant.available_slots += 1
            variant.save()

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


