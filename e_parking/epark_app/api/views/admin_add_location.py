from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import CustomUser,Location,OpeningHours
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
import requests
import calendar
from datetime import datetime

class AdminLocationAPIList(APIView):

    def get_lat_lng_from_address(address):
        print("Inside get_lat_lng_from_address")
        YOUR_API_KEY = config('YOUR_API_KEY')
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": YOUR_API_KEY
        }

        response = requests.get(base_url, params=params)
        print("response", response)
        data = response.json()
        print("data", data)

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            print("Geocoding failed. Status:", data["status"])
            return None, None

    def get(self,request):
        try:
            print("Inside get AdminLocationAPIList")
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)

            YOUR_API_KEY = config('YOUR_API_KEY')
            context = {
                YOUR_API_KEY:YOUR_API_KEY
            }
            return render(request, 'admin_select_location.html', context)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template admin_select_location.html does not exist'},
                status=404)



    def post(self, request):
        try:
            print("Inside post AdminLocationAPIList ", request)
            print("Inside post AdminLocationAPIList ", request.data)
            name = request.data["name"]
            address = request.data["address"]
            latitude = request.data.get("latitude")
            longitude = request.data.get("longitude")
            print("latitude", latitude)
            print("latitude", len(latitude))
            print("longitude", longitude)
            print("longitude", len(longitude))
            # image = request.data["image"]
            # print("image", image)

            try:
                user_email = request.session.get('email')
                user = CustomUser.objects.get(email=user_email)
                print("In")
            except ObjectDoesNotExist:
                return JsonResponse(
                    {'message': 'User not found', 'error': 'The user does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

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

            if len(latitude) == 0 and len(longitude) == 0:
                print("Lat and lng not there in request,so generate")
                YOUR_API_KEY = config('YOUR_API_KEY')
                base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                params = {
                    "address": address,
                    "key": YOUR_API_KEY
                }
                print("before request")
                response = requests.get(base_url, params=params)
                print("response", response)
                data = response.json()
                print("data", data)

                if data["status"] == "OK":
                    location = data["results"][0]["geometry"]["location"]
                    latitude = location["lat"]
                    longitude = location["lng"]

                else:
                    print("Geocoding failed. Status:", data["status"])
                    return JsonResponse(
                        {'message': 'Address not found', 'error': 'Address not found in geocode'},
                        status=status.HTTP_409_CONFLICT
                    )

            print("latitude, longitude", type(latitude), type(longitude))
            print("latitude, longitude", latitude,longitude)
            try:
                already_exist = Location.objects.get(name=name, address=address, latitude=latitude, longitude=longitude)
                print("already_exist", already_exist)
            except:
                already_exist = None


            if already_exist:
                print("already exist ,so 404")
                return JsonResponse(
                    {'message': 'Data already exists', 'error': 'The provided data already exists'},
                    status=status.HTTP_409_CONFLICT
                )
            try:
                new_location = Location(name=name, address=address, latitude=latitude, longitude=longitude)
                new_location.save()
                print("Saved sucess")
            except:
                return JsonResponse(
                    {'message': 'Location name already exists,try different', 'error': 'Location name already exists,try different'},
                    status=status.HTTP_409_CONFLICT
                )

            for day, day_name in OpeningHours.DAYS_OF_WEEK:
                print("inside")
                open_time = request.POST.get(f'{day_name.lower()}OpenTime')
                close_time = request.POST.get(f'{day_name.lower()}CloseTime')
                print("open_time", day_name,open_time)
                print("close_time", day_name, close_time)

                if open_time == "":
                    open_time = '00:00'
                if close_time == "":
                    close_time = '23:59'

                print("open_time",day_name , open_time)
                print("close_time", day_name , close_time)
                opening_hours = OpeningHours(
                    location=new_location,
                    day_of_week=day,
                    opening_time=open_time,
                    closing_time=close_time
                )
                opening_hours.save()

            # Return a success response
            response_data = {'message': 'Request processed successfully'}
            print("response_data", response_data)
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            print("cust not present")
            return JsonResponse(
                {'message': 'User not found', 'error': 'User with the provided email does not exist'},
                status=404)
        except Exception as e:
            print("In exception", e)
            return Response(
                {'message': 'An error occurred', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdminGetLocationAPIList(APIView):

        def get(self, request):
            try:
                print("Inside get AdminEditLocationAPIList")
                user_email = request.session.get('email')
                user = CustomUser.objects.get(email=user_email)
                if user.is_superuser:
                    loc_obj = Location.objects.all()
                    print("loc_obj", loc_obj)
                    resulting_list = []
                    for data in loc_obj:
                        resulting_dict = {
                            "location_id":data.id,
                            "name": data.name,
                            "address": data.address,
                            "latitude": data.latitude,
                            "longitude": data.longitude

                        }
                        resulting_list.append(resulting_dict)
                    context = {"resulting_list" : resulting_list}
                    print("context", context)
                    return render(request, 'admin_get_location.html', context)
                else:
                    return JsonResponse(
                        {'message': 'User is not a admin', 'error': 'User is not a admin'},
                        status=404)
            except TemplateDoesNotExist:
                return JsonResponse(
                    {'message': 'Template not found',
                     'error': 'The template admin_get_location.html does not exist'},
                    status=404)
            except CustomUser.DoesNotExist:
                return JsonResponse(
                    {'message': 'User not found', 'error': 'User not found'},
                    status=404)


class AdminEditLocationAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get admin AdminEditLocationAPIList")
            user_email = request.session.get('email')
            print("user_email", user_email)
            user = CustomUser.objects.get(email=user_email)
            print("*********************************** super",user.is_superuser)
            if user.is_superuser:
                address = request.GET.get('address')

                name = request.GET.get('name')
                latitude = request.GET.get('latitude')
                address = request.GET.get('address')
                longitude = request.GET.get('longitude')
                location_id = request.GET.get('location_id')


                opening_hours_list = []
                loc_obj = Location.objects.get(id=location_id)
                opening_hours  = OpeningHours.objects.filter(location=loc_obj)
                for hours in opening_hours:
                    print("hours", hours)
                    opening_time_str = hours.opening_time.strftime('%H:%M')
                    print("opening_time_str", opening_time_str)

                    closing_time_str = hours.closing_time.strftime('%H:%M')
                    print("closing_time_str", closing_time_str)

                    day_of_week = hours.day_of_week
                    opening_hours_list.append({
                        'day_of_week': calendar.day_name[day_of_week] ,
                        'opening_time': opening_time_str,
                        'closing_time': closing_time_str,
                    })


                context = {
                    "location_id": location_id,
                    "name": name,
                    "address": address,
                    "latitude": latitude,
                    "longitude": longitude,
                    "opening_hours":opening_hours_list
                }

                print("context", context)

                return render(request, 'admin_edit_location.html', context)
            else:

                return JsonResponse(
                    {'message': 'User is not admin', 'error': 'User is not admin'},
                    status=404)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found',
                 'error': 'The template admin_edit_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

    def get_day_index(self,day_name):
        DAYS_OF_WEEK = (
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        )
        for index, name in DAYS_OF_WEEK:
            if name == day_name:
                return index
        return None

    def patch(self, request):

        try:
            print(" PATCH admin Location request", request)
            print(" patch admin location request", request.data)

            name = request.data["name"]
            address = request.data["address"]
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            location_id = request.data["location_id"]
            opening_times = request.POST.getlist('OpenTime')
            print("opening_times", opening_times)

            closing_times = request.POST.getlist('CloseTime')
            print("closing_times", closing_times)

            loc_obj = Location.objects.get(id=location_id)
            loc_obj.name = name
            loc_obj.latitude = latitude
            loc_obj.address = address
            loc_obj.longitude = longitude
            loc_obj.save()
            print("Location saved")
            for day_index, opening_time, closing_time in zip(
                    [self.get_day_index('Monday'), self.get_day_index('Tuesday'), self.get_day_index('Wednesday'),
                     self.get_day_index('Thursday'), self.get_day_index('Friday'), self.get_day_index('Saturday'),
                     self.get_day_index('Sunday')], opening_times, closing_times):
                print("day_index, opening_time, closing_time", day_index, opening_time, closing_time)

                opening_hours, created = OpeningHours.objects.get_or_create(location=loc_obj, day_of_week=day_index)
                opening_hours.opening_time = opening_time
                opening_hours.closing_time = closing_time
                opening_hours.save()
                print("One save")



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
