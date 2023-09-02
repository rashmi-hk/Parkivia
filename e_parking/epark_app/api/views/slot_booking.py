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
import pytz


class SlotBookingAPIList(APIView):



    def get(self, request):
        print("Inside slot_booking get", request)
        print("Inside slot_booking get", request.data)
        try:
            user_email = request.session.get('email')
            print("user_email",user_email)
            user = CustomUser.objects.get(email=user_email)

            user_location = user.parking_lot_location


            # all_booked_obj = SlotBooking.objects.filter(slot__parking_lot_location=user_location)
            all_booked_obj = SlotBooking.objects.filter(
                slot__location=user_location
            )


            resulting_list = []
            for data in all_booked_obj:
                slot_obj = SlotDetail.objects.get(id = data.slot.id)
                # variant_data = data.slot.slot_variants

                variant_result_list = []

                for variant in slot_obj.slot_variants.filter(vehicle_type = data.vehicle_type):
                    print("@#@#@#", variant)
                    variant_dict = {

                     }
                    variant_result_list.append(variant_dict)
                print("variant_result_list", variant_result_list)


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
                             "is_bill_generated": data.is_bill_generated,
                             }

                resulting_list.append(data_dict)

            context = {'slot_detail': resulting_list,
                       }
            print("context", context)
            # if user.is_superuser:
            #     print("User is admin")
            #     return render(request, 'admin_booked_slot_detail.html',context)
            # else:
            print("user is staff")
            return render(request, 'booked_slot_detail.html',context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside slot_booking post", request)
        print("Inside slot_booking post user", request.user)
        print("Inside slot_booking post", request.data)
        try:
            user_email = request.session.get('email')


            user = CustomUser.objects.get(email=user_email)
           # User with the provided email doesn't exist


            if not user.is_authenticated:
                print("User not authenticated")
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                    status=status.HTTP_401_UNAUTHORIZED)


            print("User athenticated n superuser")
            slot = request.data["slot"]
            check_in_time = request.data["check_in_time"]
            vehicle_number = request.data["vehicle_number"]
            vehicle_type = request.data["vehicle_type"]
            print("slot", slot)

            slot_detail_obj = SlotDetail.objects.filter(id=slot).first()
            print("***slot_detail_obj", slot_detail_obj)
            new_slot_booking = SlotBooking()
            new_slot_booking.slot = slot_detail_obj
            new_slot_booking.check_in_time = check_in_time
            new_slot_booking.vehicle_number = vehicle_number
            new_slot_booking.vehicle_type = vehicle_type
            new_slot_booking.save()

            print("Row created")

            variants = SlotDetailVariant.objects.filter(slot__id=slot_detail_obj.id,vehicle_type=vehicle_type)
            print("variants", len(variants))
            print("variants",variants)
            if len(variants):
                print("Slot available*********************************************")
                # Iterate through the variants and update available_slots
                for variant in variants:
                    print("Inside for",variant.available_slots)
                    if variant.available_slots:
                        variant.available_slots -= 1
                        variant.save()
                        print("saved sucess")
                    else:
                        response_data = {'message': 'Parking slot not availables'}
                        return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)

                response_data = {'message': 'Request processed successfully'}
                return JsonResponse(response_data, status=status.HTTP_201_CREATED)
            else:
                print("Slot not available************************")
                response_data = {'message': 'Parking slot not availables'}
                return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)

        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)




class SlotBookingFormAPIList(APIView):

    def get(self, request):
        print("Inside SlotBookingFormAPIList get", request)
        print("Inside SlotBookingFormAPIList get", request.data)
        try:
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)
            vehicle_choices = CustomUser.VEHICLE_CHOICES
            if user.is_superuser:
                slot_details = SlotDetail.objects.all()
                print("############### slot_variants ", slot_details)
            else:

                slot_details = SlotDetail.objects.filter(location=user.parking_lot_location)
                print("############### slot_variants ", slot_details)

            unique_vehicle_types = set()


            slot_detail_list = []
            for slot_data in slot_details:
                slot_variants = SlotDetailVariant.objects.filter(slot=slot_data)
                slot_vehicle_types = slot_variants.values_list("vehicle_type", flat=True)
                unique_vehicle_types.update(slot_vehicle_types)
                slot_detail_dict = {"slot_name": slot_data.name,
                                    "slot_id": slot_data.id,
                                    "location": slot_data.location,
                                    "vehicle_choices": slot_vehicle_types}
                slot_detail_list.append(slot_detail_dict)

            print("datetime", datetime.now())
            context = {
                       'slot_detail_list': slot_detail_list,
                       'all_vehicle_types': unique_vehicle_types,
                        "current_datetime" : datetime.now().strftime('%Y-%m-%dT%H:%M')
                        }

            print("context",context)
            if user.is_superuser:
                return render(request, 'admin_slot_booking.html', context)
            else:
                return render(request, 'slot_booking.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)


class SlotBookingEditAPIList(APIView):


    def get(self, request):
        print("Inside SlotBookingEditAPIList get", request)

        format_string = "%Y-%m-%d %H:%M:%S"
        try:
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)

            slot = request.GET.get('slot')
            check_in_time = request.GET.get('check_in_time')

            check_out_time = request.GET.get('check_out_time')
            vehicle_number = request.GET.get('vehicle_number')
            vehicle_type = request.GET.get('vehicle_type')
            amount = request.GET.get('amount')

            booking_id = request.GET.get('booking_id')


            date_time_obj = parser.parse(check_in_time)

            check_in_date_time_obj = date_time_obj.strftime(format_string)
            print(date_time_obj)

            context = {
               'slot': slot,
               'check_in_time': check_in_date_time_obj,
                "check_out_time": check_out_time,
                "vehicle_number": vehicle_number,
                "vehicle_type": vehicle_type,
                "amount": amount,
                "booking_id": booking_id,
                "current_datetime": datetime.now().strftime('%Y-%m-%dT%H:%M')
            }
            if user.is_superuser:
                print("super user")
                return render(request, 'admin_booked_slot_edit.html', context)
            else:
                print("Not super user")
                return render(request, 'booked_slot_edit.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)




    def patch(self, request):

        try:
            print(" PATCH SLOT BOOKING request", request)
            print(" patch slot booking request", request.data)


            check_in_time = request.data['check_in_time']
            check_out_time = request.data['check_out_time']
            vehicle_number = request.data['vehicle_number']
            vehicle_type = request.data['vehicle_type']
            booking_id = request.data['booking_id']
            check_in_time_format = "%d-%m-%Y, %H:%M"




            # check_in_time_obj = parser.parse(check_in_time)
            # print("Parsed check-in time:", check_in_time)
            check_in_time_obj = parser.parse(check_in_time)
            print("Parsed check-in time:", check_in_time_obj)

            slot_booking_obj = SlotBooking.objects.get(id=booking_id)
            print("!!!!1")
            check_out_time_obj = 0
            payable_amount = 0
            if check_out_time:
                # check_out_time_obj = parser.parse(check_out_time)
                # print("check_out_time_obj", check_out_time_obj)
                check_out_time_obj = parser.parse(check_out_time)
                print("check_out_time_obj", check_out_time_obj)

                duration = check_out_time_obj - check_in_time_obj
                print("duration", duration)

                total_hours = duration.total_seconds() / 3600
                print("total_hours", total_hours)

                slot_obj = SlotDetailVariant.objects.filter(slot=slot_booking_obj.slot , vehicle_type=vehicle_type).first()
                print("$$$$$$2", slot_obj)

                rate_1_day = round(slot_obj.daily_rate)
                rate_1_hour = round(slot_obj.hourly_rate_1_hour)
                rate_3_hours = round(slot_obj.hourly_rate_3_hours)
                rate_6_hours = round(slot_obj.hourly_rate_6_hours)
                rate_12_hours = round(slot_obj.hourly_rate_12_hours)

                print("rate_1_day",rate_1_day)
                print("rate_1_hour",rate_1_hour)
                print("rate_3_hours",rate_3_hours)
                print("rate_6_hours",rate_6_hours)
                print("rate_12_hours",rate_12_hours)

                # Assuming total_hours is the total duration in hours
                payable_amount = 0

                if total_hours >= 24:
                    # Calculate for full days (24 hours)
                    full_days = total_hours // 24
                    payable_amount += full_days * rate_1_day
                    total_hours %= 24

                if total_hours >= 12:
                    # Calculate for 12-hour slots
                    twelve_hour_slots = total_hours // 12
                    payable_amount += twelve_hour_slots * rate_12_hours
                    total_hours %= 12

                if total_hours >= 6:
                    # Calculate for 6-hour slots
                    six_hour_slots = total_hours // 6
                    payable_amount += six_hour_slots * rate_6_hours
                    total_hours %= 6

                if total_hours >= 3:
                    # Calculate for 3-hour slots
                    three_hour_slots = total_hours // 3
                    payable_amount += three_hour_slots * rate_3_hours
                    total_hours %= 3

                # Calculate for remaining hours using the hourly rate
                payable_amount += total_hours * rate_1_hour

                print("payable_amount", payable_amount)


            else:
                print("check_out_time not specified")

            check_in_time_aware = timezone.make_aware(check_in_time_obj)
            check_out_time_aware = timezone.make_aware(check_out_time_obj) if check_out_time_obj else None
            slot_booking_obj.check_in_time = check_in_time_aware
            slot_booking_obj.check_out_time = check_out_time_aware
            slot_booking_obj.vehicle_number = vehicle_number
            slot_booking_obj.vehicle_type = vehicle_type
            slot_booking_obj.amount = round(payable_amount)
            slot_booking_obj.save()
            print("Saved sucess")
            return JsonResponse({'message': 'Staff location updated successfully'}, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:

            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
