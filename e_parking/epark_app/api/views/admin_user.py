from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
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
class AdminUserCreateAPIList(APIView):

    def get(self,request):
        print("Inside admin get user")
        all_location = Location.objects.all()
        vehicle_choices = CustomUser.VEHICLE_CHOICES

        context = {"all_location" : all_location,
                   "vehicle_choices" : vehicle_choices}

        return render(request, 'admin_add_user.html', context)

class AdminUserAPIList(APIView):
    def get(self, request, user_id=None):
        try:
            all_location = Location.objects.all()
            vehicle_choices = CustomUser.VEHICLE_CHOICES

            context = {
                "all_location": all_location,
                "vehicle_choices": vehicle_choices
            }

            if user_id is None:
                print("Inside admin get all users")
                user_data = CustomUser.objects.all()
                resulting_list = []
                for user in user_data:
                    resulting_dict = {
                        "user_id" : user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone_number': user.phone_number,
                        'is_verified': user.is_verified,
                        'address': user.address,
                        'otp': user.otp,
                        'is_logged_in': user.is_logged_in,
                        'display_picture': user.display_picture,
                        'vehicle_type': user.vehicle_type,
                        'parking_lot_location': user.parking_lot_location,
                    }
                    resulting_list.append(resulting_dict)

                context = {"resulting_list" : resulting_list}
                return render(request, 'admin_user_edit.html', context)
            else:

                print(f"Inside admin get single user: {user_id}")
                user_data = CustomUser.objects.get(id=user_id)
                resulting_dict = {
                    "user_id": user_data.id,
                    'username': user_data.username,
                    'email': user_data.email,
                    'phone_number': user_data.phone_number,
                    'is_verified': user_data.is_verified,
                    'address': user_data.address,
                    'display_picture': user_data.display_picture,
                    'vehicle_type': user_data.vehicle_type,
                    'parking_lot_location': user_data.parking_lot_location,
                    "all_location": all_location,
                    "is_staff": user_data.is_staff,
                    "is_admin": user_data.is_admin,
                    "vehicle_choices": vehicle_choices,
                }
                context = {"resulting_list": resulting_dict}
                print("context single user", context)
                return render(request, 'admin_single_user_edit.html', context)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:
            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


    def patch(self, request):

            try:
                print(" PATCH admin user request", request)
                print(" patch admin user request", request.data)

                user_id = request.data["user_id"]
                email = request.data["email"]
                username = request.data["username"]
                phone_number = request.data["phone_number"]
                is_staff = request.data.get("is_staff")
                is_admin = request.data.get("is_admin")
                address = request.data["address"]
                vehicle_type = request.data["vehicle_type"]
                parking_lot_location = request.data["parking_lot_location"]


                try:
                    if user_id:
                        cust_obj = CustomUser.objects.get(id=user_id)
                        cust_obj.email = email
                        cust_obj.username = username
                        cust_obj.phone_number = phone_number
                        cust_obj.is_staff = is_staff
                        cust_obj.is_admin = is_admin
                        cust_obj.address = address
                        cust_obj.vehicle_type = vehicle_type
                        cust_obj.parking_lot_location = parking_lot_location
                        cust_obj.save()
                        print("Edited sucessfully")
                except:
                    print("User Editing is done")

                print("Saved sucess")
                return JsonResponse({'message': 'location updated successfully'}, status=status.HTTP_201_CREATED)

            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'}, status=404)
            except Exception as e:

                print('Unexpected error occurred:', str(e))
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)




