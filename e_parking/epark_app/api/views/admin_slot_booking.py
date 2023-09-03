from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotBooking,SlotDetail,SlotDetailVariant
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
from dateutil import parser
from datetime import datetime
from decimal import Decimal



class AdminSlotBookingAPIList(APIView):


    def get(self, request):
        print("Inside AdminSlotBookingAPIList get", request)
        print("Inside AdminSlotBookingAPIList get", request.data)
        try:
            user_email = request.session.get('email')
            print("user_email",user_email)
            user = CustomUser.objects.get(email=user_email)

            all_booked_obj = SlotBooking.objects.all()


            resulting_list = []
            for data in all_booked_obj:
                slot_obj = SlotDetail.objects.get(id = data.slot.id)
                # variant_data = data.slot.slot_variants

                variant_result_list = []

                for variant in slot_obj.slot_variants.filter(vehicle_type = data.vehicle_type):
                    print("@#@#@#", variant)
                    variant_dict = {
                     "hourly_amount": variant.hourly_rate
                     }
                    variant_result_list.append(variant_dict)
                print("variant_result_list", variant_result_list)
                print("datetime", datetime.now())

                data_dict = {"slot": data.slot,
                             "slot_id": data.id,
                             "location": slot_obj.location,
                             "check_in_time": data.check_in_time,
                             "check_out_time": data.check_out_time,
                             "vehicle_number": data.vehicle_number,
                             "variant_result_list": variant_result_list,
                             "vehicle_type": data.vehicle_type,
                             "amount":data.amount,
                             "booking_id":data.id,
                             "slot_detail_id": slot_obj.id,
                             "is_bill_generated":data.is_bill_generated,

                             }

                resulting_list.append(data_dict)

            context = {'slot_detail': resulting_list,
                       # 'slot_detail_list': slot_detail_list,
                       # 'all_vehicle_types': all_vehicle_types
                       }
            print("context", context)

            print("User is admin")
            return render(request, 'admin_booked_slot_detail.html',context)


        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)


