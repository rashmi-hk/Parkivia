from rest_framework.views import APIView
from django.shortcuts import render, redirect
import json
from ...models import CustomUser,Location, SlotDetail, SlotDetailVariant
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
from django.utils.crypto import get_random_string
from django.template import TemplateDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


class AdminGetSlotDetailAPIList(APIView):

        def get(self, request):
            try:
                print("Inside get AdminGetSlotDetailAPIList")
                slot_detail_obj = SlotDetail.objects.all()
                print("slot_detail_obj", slot_detail_obj)
                resulting_list = []
                for data in slot_detail_obj:


                    resulting_dict = {
                        "slot_detail_id":data.id,
                        "name": data.name,
                        "opening_hours": data.opening_hours,
                        "location": data.location,


                    }
                    resulting_list.append(resulting_dict)
                context = {"resulting_list" : resulting_list}
                print("context", context)
                return render(request, 'admin_get_slot_detail.html', context)
            except TemplateDoesNotExist:
                return JsonResponse(
                    {'message': 'Template not found',
                     'error': 'The template admin_get_slot_detail.html does not exist'},
                    status=404)


class AdminEditSlotDetailAPIList(APIView):

    def get(self, request):
        try:
            print("Inside post AdminEditSlotDetailAPIList", request)


            slot_detail_id = request.GET.get('slot_id')
            print("slot_detail_id", slot_detail_id)
            name = request.GET.get('name')
            print("name", name)
            opening_hours = request.GET.get('opening_hours')
            location = request.GET.get('location')
            slot_data_obj = SlotDetail.objects.get(id = slot_detail_id)
            slot_variant_obj = slot_data_obj.slot_variants.all()

            print("slot_detail_id", slot_detail_id)

            var_list = []
            for var_data in slot_variant_obj:
               var_dict = { "slot" : var_data.slot,
                            "var_slot_id": var_data.id,
                            "capacity": var_data.capacity,
                            "available_slots": var_data.available_slots,
                            "vehicle_type": var_data.vehicle_type,
                            "hourly_rate": var_data.hourly_rate}

               var_list.append(var_dict)

            context = {
                'slot_detail_id': slot_detail_id,
                'name': name,
                'opening_hours': opening_hours,
                'location': location,
                'slot_variants':var_list}


            print("context", context)
            return render(request, 'admin_edit_slot_detail.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found',
                 'error': 'The template admin_edit_location.html does not exist'},
                status=404)

    def patch(self, request):

        try:
            print(" PATCH admin slot detail request", request)
            print(" patch admin slot detail  request", request.data)

            slot_detail_id = request.data["slot_detail_id"]
            name = request.data["name"]
            opening_hours = request.data["opening_hours"]
            location = request.data["location"]
            slot = request.data["slot"]
            capacity = request.data["capacity"]
            available_slots = request.data["available_slots"]
            vehicle_type = request.data["vehicle_type"]
            hourly_rate = request.data["hourly_rate"]
            var_slot_id = request.data["var_slot_id"]

            if slot_detail_id:
                SlotDetail.objects.get(id=slot_detail_id,)



            loc_obj = Location.objects.get(id=location_id)
            loc_obj.name = name
            loc_obj.latitude = latitude
            loc_obj.address = address
            loc_obj.longitude = longitude
            loc_obj.save()

            print("Saved sucess")
            return JsonResponse({'message': 'location updated successfully'}, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:

            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    def delete(self, request):

        print("inside delete Location item", request.data)
        print("inside delete Location item", request)

        location_id = name = request.GET.get('location_id')

        print("location_id", location_id)

        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)

        if not user.is_authenticated:
            print("User not authenticated")
            return JsonResponse(
                {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_superuser:
            print("user not superuser")
            return JsonResponse(
                {'message': 'Unauthorized', 'error': 'You do not have permission to access this resource'},
                status=status.HTTP_403_FORBIDDEN)

        try:
            location_item = Location.objects.get(id=location_id)
            print("location_item", location_item)

            if location_item:
                location_item.delete()

            return HttpResponse("location deleted successfully.")

        except Location.DoesNotExist:
            return HttpResponseBadRequest("Location not found.")
