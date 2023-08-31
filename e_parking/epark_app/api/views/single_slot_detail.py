from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotDetail, SlotDetailVariant
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
import requests

class SingleSlotAPIList(APIView):

    def get_address_from_latlng(self,lat, lng, api_key):
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lng}",
            "key": api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("results"):
            formatted_address = data["results"][0]["formatted_address"]
            return formatted_address
        else:
            return "Address not found"


    def get(self, request):
        try:
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)
            print("Data", request)
            print("Data", request.GET)
            current_lat = request.GET.get('lat')
            current_lng = request.GET.get('lng')
            lat = request.GET.get('user_lat')
            lng = request.GET.get('user_lng')
            location_id = request.GET.get('location_id')

            slot_detail_obj = SlotDetail.objects.filter(location=location_id)
            print("slot_detail_obj", slot_detail_obj)

            grouped_data = {}  # Initialize a dictionary for grouping

            for data in slot_detail_obj:
                for variant in SlotDetailVariant.objects.filter(slot__id=data.id):
                    # Update available_slots and vehicle_type
                    variant_dict = {
                        "available_slots": variant.available_slots,
                        "vehicle_type": variant.vehicle_type,
                        "capacity": variant.capacity,

                        "name": variant.slot,
                        "latitude":lat,
                        "longitude": lng,
                        "hourly_rate_1_hour" : variant.hourly_rate_1_hour,
                        "hourly_rate_3_hours" : variant.hourly_rate_3_hours,
                        "hourly_rate_6_hours" : variant.hourly_rate_6_hours,
                        "hourly_rate_12_hours" : variant.hourly_rate_12_hours,
                        "daily_rate" : variant.daily_rate
                    }

                    # Group data by slot name
                    if variant.slot in grouped_data:
                        grouped_data[variant.slot].append(variant_dict)
                    else:
                        grouped_data[variant.slot] = [variant_dict]

            # Create a list of dictionaries with grouped data
            resulting_list = [
                {
                    "name": slot_name,
                    "variant_dict": variant_list,

                    "location": data.location,  # Include location
                }
                for slot_name, variant_list in grouped_data.items()
            ]

            context = {'slot_detail': resulting_list,
                       'current_lat': current_lat,
                       'current_lng': current_lng
                       }
            print("context", context)
            return render(request, 'user_slot_detail.html', context)

        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template user_slot_detail.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)
