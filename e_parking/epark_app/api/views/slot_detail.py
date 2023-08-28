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

            slot_detail_obj = SlotDetail.objects.filter(location=user.parking_lot_location)
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
                    "hourly_rate" : variant.hourly_rate,
                    "name": variant.slot,
                    variant.vehicle_type + str("percentage"): percent_val * 100}
                    variant_list.append(variant_dict)


                data_dict = {

                              "variant_dict": variant_list,
                             "opening_hours": data.opening_hours,
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

    # def post(self, request):
    #     print("Inside location post", request)
    #     print("Inside location post user", request.user)
    #     print("Inside location post", request.data)
    #     try:
    #         user_email = request.session.get('email')
    #
    #
    #         user = CustomUser.objects.get(email=user_email)
    #        # User with the provided email doesn't exist
    #
    #
    #         if not user.is_authenticated:
    #             print("User not authenticated")
    #             return JsonResponse(
    #                 {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
    #                 status=status.HTTP_401_UNAUTHORIZED)
    #
    #
    #
    #         print("User athenticated n superuser")
    #         address = request.data["address"]
    #         print("address", address)
    #
    #         name = request.data["name"]
    #         print("name", name)
    #
    #
    #         new_location = Location()
    #         new_location.address = address
    #         new_location.name = name
    #         new_location.save()
    #         response_data = {'message': 'Request processed successfully'}
    #         return JsonResponse(response_data, status=status.HTTP_200_OK)
    #
    #     except CustomUser.DoesNotExist:
    #         # If the user does not exist, you can handle it accordingly
    #         # For example, you might want to return an error response
    #         return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
    #                             status=404)
