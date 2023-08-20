from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotDetail
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

            lat = request.GET.get('lat')
            lng = request.GET.get('lng')
            location_id = request.GET.get('location_id')

            slot_detail_obj = SlotDetail.objects.filter(location=location_id)
            grouped_data = {}  # Initialize a dictionary for grouping

            for data in slot_detail_obj:
                for variant in data.slot_variants.all():
                    # Update available_slots and vehicle_type
                    variant_dict = {
                        "available_slots": variant.available_slots,
                        "vehicle_type": variant.vehicle_type,
                        "capacity": variant.capacity,
                        "hourly_rate": variant.hourly_rate,
                        "name": variant.slot,
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
                    "opening_hours": data.opening_hours,  # Include opening_hours
                    "location": data.location,  # Include location
                }
                for slot_name, variant_list in grouped_data.items()
            ]

            context = {'slot_detail': resulting_list}
            print("context", context)
            return render(request, 'user_slot_detail.html', context)

        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template user_slot_detail.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)