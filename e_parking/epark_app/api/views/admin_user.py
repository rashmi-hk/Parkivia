from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
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
class AdminUserCreateAPIList(APIView):

    def get(self,request):
        try:
            print("Inside admin get user")
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)
            all_location = Location.objects.all()
            vehicle_choices = CustomUser.VEHICLE_CHOICES

            context = {"all_location" : all_location,
                       "vehicle_choices" : vehicle_choices}

            return render(request, 'admin_add_user.html', context)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            print("Error:", e)
            return render(request, 'admin_add_user.html', {'errors': str(e)})  # Render HTML

    def post(self, request):
        print("Inside post",request)
        print("Inside post",request.data)
        try:

            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            phone_number = request.data.get('phone_number')
            is_superuser_status = request.data.get('is_superuser')
            address = request.data.get('address')
            vehicle_type = request.data.get('vehicle_type')
            parking_lot_location = request.data.get('parking_lot_location')
            print("parking_lot_location", parking_lot_location)


            is_staff_status = request.data.get('is_staff')
            user_data = {}
            print("is_staff_status",is_staff_status)
            if is_staff_status:
                location_obj = Location.objects.get(id=parking_lot_location)
                user_data.update({"parking_lot_location":location_obj})
                is_staff = True
            else:
                is_staff = False

            if is_superuser_status:
                is_superuser = True
            else:
                is_superuser = False

            print("is_superuser", is_superuser)
            print("Before create_user")

            user_data.update({ "username":username,
                "email":email,
                "password":password,
                "phone_number":phone_number,
                "is_staff":is_staff,
                "is_superuser":is_superuser,
                "address":address,
                "vehicle_type":vehicle_type,
                "is_verified":True
                })
            if is_superuser:
                new_user = CustomUser.objects.create_superuser(**user_data)
            else:
                new_user = CustomUser.objects.create_user(**user_data)


            print("After create_user")
            all_location = Location.objects.all()
            vehicle_choices = CustomUser.VEHICLE_CHOICES

            context = {"all_location": all_location,
                       "vehicle_choices": vehicle_choices}
            return render(request, 'admin_add_user.html',context)  # Render HTML template for success
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:
            print("Error:", e)
            return render(request, 'admin_add_user.html', {'errors': str(e)})  # Render HTML


class AdminUserAPIList(APIView):
    def get(self, request, user_id=None):
        try:
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)
            if user.is_superuser:
                all_location = Location.objects.all()
                vehicle_choices = CustomUser.VEHICLE_CHOICES

                context = {
                    "all_location": all_location,
                    "vehicle_choices": vehicle_choices
                }

                if user_id is None:
                    print("Inside admin get all users")
                    user_data = CustomUser.objects.filter(is_staff=True,is_superuser=False)
                    resulting_list = []
                    for user in user_data:
                        resulting_dict = {
                            "user_id" : user.id,
                            "is_staff":user.is_staff,
                            "is_superuser":user.is_superuser,
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
                    print("**&*")
                    print("user_data is staff ****", user_data.is_superuser)
                    resulting_dict = {
                        "user_id": user_data.id,
                        "is_staff": user_data.is_staff,
                        "is_admin": user_data.is_superuser,
                        'username': user_data.username,
                        'email': user_data.email,
                        'phone_number': user_data.phone_number,
                        'is_verified': user_data.is_verified,
                        'address': user_data.address,
                        'display_picture': user_data.display_picture,
                        'vehicle_type': user_data.vehicle_type,
                        'parking_lot_location': user_data.parking_lot_location,
                        "all_location": all_location,
                        "vehicle_choices": vehicle_choices,
                    }
                    context = {"resulting_list": resulting_dict}
                    print("context single user", context)
                    return render(request, 'admin_single_user_edit.html', context)
            else:
                return JsonResponse(
                    {'message': 'User not authenticated', 'error': 'User not authenticated'},
                    status=403)

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
                print("is_admin",is_admin)
                address = request.data["address"]
                vehicle_type = request.data["vehicle_type"]
                parking_lot_location = request.data["parking_lot_location"]


                try:
                    if user_id is not None:
                        cust_obj = CustomUser.objects.get(id=user_id)
                        cust_obj.email = email
                        cust_obj.username = username
                        cust_obj.phone_number = phone_number
                        print("**********",is_staff)
                        if is_staff:
                            print("Staff on")
                            cust_obj.is_staff = True
                            location_obj = Location.objects.get(id=parking_lot_location)
                            cust_obj.parking_lot_location = location_obj

                        else:
                            print("staff off")
                            cust_obj.is_staff = False

                        if is_admin:
                            cust_obj.is_superuser = True
                        else:
                            print("staff off")
                            cust_obj.is_superuser = False

                        cust_obj.is_admin = is_admin
                        cust_obj.address = address
                        cust_obj.vehicle_type = vehicle_type

                        cust_obj.save()
                        print("Edited sucessfully")
                except Exception as err:
                    print('Unexpected error occurred:', str(err))
                    print("User Editing is done")

                print("Saved sucess")
                return JsonResponse({'message': 'location updated successfully'}, status=status.HTTP_201_CREATED)

            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'}, status=404)
            except Exception as e:

                print('Unexpected error occurred:', str(e))
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    def delete(self,request):
        print("Inside try",request)
        print("Inside try",request.data)
        user_id = request.GET.get('user_id')
        print("user_id", user_id)

        try:
            user_detail = CustomUser.objects.get(id=user_id)
            user_detail.delete()
            return HttpResponse("User deleted successfully.")
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:

            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)





