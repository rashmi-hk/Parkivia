from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotBooking,SlotDetail
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
class SlotBookingAPIList(APIView):



    def get(self, request):
        print("Inside slot_booking get", request)
        print("Inside slot_booking get", request.data)
        try:
            all_booked_obj = SlotBooking.objects.all()
            slot_detail = SlotDetail.objects.all()
            all_vehicle_types = [choice[0] for choice in SlotDetail.VEHICLE_CHOICES]
            slot_detail_list = []
            for slot_data in slot_detail:
                slot_detail_dict = {"slot_name": slot_data.name,
                                    "slot_id" : slot_data.id,
                                    }
                slot_detail_list.append(slot_detail_dict)




            resulting_list = []
            for data in all_booked_obj:

                data_dict = {"slot": data.slot,
                             "check_in_time": data.check_in_time,
                             "check_out_time": data.check_out_time,
                             "vehicle_number": data.vehicle_number,
                             "vehicle_type": data.vehicle_type,
                             "amount":data.amount,
                             "hourly_amount": data.slot.hourly_rate}

                resulting_list.append(data_dict)

            context = {'slot_detail': resulting_list,
                       'slot_detail_list': slot_detail_list,
                       'all_vehicle_types': all_vehicle_types}
            print("context", context)
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
            new_slot_booking = SlotBooking()
            new_slot_booking.slot = slot_detail_obj
            new_slot_booking.check_in_time = check_in_time
            new_slot_booking.vehicle_number = vehicle_number
            new_slot_booking.vehicle_type = vehicle_type
            new_slot_booking.save()
            print("saved sucess")
            response_data = {'message': 'Request processed successfully'}
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)

    def delete(self, request):

        print("inside delete Location item", request.data)

        location_id = request.data['location_id']

        print("location_id", location_id)

        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)

        if not user.is_authenticated:
            print("User not authenticated")
            return JsonResponse(
                {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                status=status.HTTP_401_UNAUTHORIZED)




        try:
            location_item = Location.objects.get(id=location_id)
            print("location_item", location_item)

            if location_item:
                    location_item.delete()

            return HttpResponse("location deleted successfully.")

        except Location.DoesNotExist:
            return HttpResponseBadRequest("Location not found.")


class SlotBookingFormAPIList(APIView):

    def get(self, request):
        print("Inside SlotBookingFormAPIList get", request)
        print("Inside SlotBookingFormAPIList get", request.data)
        try:
            slot_detail = SlotDetail.objects.all()
            all_vehicle_types = [choice[0] for choice in SlotDetail.VEHICLE_CHOICES]
            slot_detail_list = []
            for slot_data in slot_detail:
                slot_detail_dict = {"slot_name": slot_data.name,
                                    "slot_id": slot_data.id}
                slot_detail_list.append(slot_detail_dict)

            context = {
                       'slot_detail_list': slot_detail_list,
                       'all_vehicle_types': all_vehicle_types}

            return render(request, 'slot_booking.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)


class SlotBookingEditAPIList(APIView):

    def get(self, request):
        print("Inside SlotBookingEditAPIList get", request)
        print("Inside SlotBookingEditAPIList get",  )
        format_string = "%d-%m-%Y, %H:%M"
        try:
            slot = request.GET.get('slot')
            check_in_time = request.GET.get('check_in_time')

            check_out_time = request.GET.get('check_out_time')
            vehicle_number = request.GET.get('vehicle_number')
            vehicle_type = request.GET.get('vehicle_type')
            amount = request.GET.get('amount')
            hourly_rate = request.GET.get('hourly_rate')

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
                "hourly_rate": hourly_rate,
            }

            return render(request, 'booked_slot_edit.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)