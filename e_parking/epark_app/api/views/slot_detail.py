from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotDetail,SlotDetailVariant
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
from django.core.serializers import serialize

class SlotDetailAPIList(APIView):


    def get(self, request):
        print("Inside SlotDetailAPIList get", request)
        print("Inside SlotDetailAPIList get", request.data)
        try:
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)
            print("location of staff", user.parking_lot_location)

            slot_detail_obj = SlotDetail.objects.filter(location=user.parking_lot_location)
            print("slot_detail_obj", slot_detail_obj)
            resulting_list = []
            for data in slot_detail_obj:
                variant_list = []
                slot_variant_obj = SlotDetailVariant.objects.filter(slot__id=data.id)

                for variant in slot_variant_obj:
                    # Update available_slots and vehicle_type
                    percent_val  = variant.available_slots/variant.capacity
                    variant_dict = {"available_slots" : variant.available_slots,
                    "vehicle_type" : variant.vehicle_type,
                    "capacity" :  variant.capacity,
                    "hourly_rate_1_hour": round(variant.hourly_rate_1_hour),
                    "hourly_rate_3_hours": round(variant.hourly_rate_3_hours),
                    "hourly_rate_6_hours": round(variant.hourly_rate_6_hours),
                    "hourly_rate_12_hours": round(variant.hourly_rate_12_hours),
                    "daily_rate": round(variant.daily_rate),
                    "name": variant.slot,
                    variant.vehicle_type + str("percentage"): percent_val * 100}
                    variant_list.append(variant_dict)


                data_dict = {

                              "variant_dict": variant_list,

                             "location": data.location}

                resulting_list.append(data_dict)

            context = {'slot_detail': resulting_list}
            print("context", context)
            return render(request, 'slot_detail.html',context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)


