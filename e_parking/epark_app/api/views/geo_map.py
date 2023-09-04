
import logging
import googlemaps
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from ...models import CustomUser,Location
import geocoder
from decouple import config
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
LOGGER = logging.getLogger(__name__)


class GMapsGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """

    def get(self, request):
        """
        Geocode the given address
        """
        try:
            print("Inside: first *****", self.__class__.__name__)
            print("Request params: ", request)
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)


            address = request.GET.get('address')

            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')
            current_latitude = request.GET.get('current_lat')
            current_longitude = request.GET.get('current_lng')
            print("***********", latitude,longitude)

            end_location = 0
            if latitude and longitude:
                lat = float(latitude)
                long = float(longitude)
                end_location = (lat, long)

            start_location = 0
            if current_latitude and current_longitude:
                lat = float(current_latitude)
                long = float(current_longitude)
                start_location = (lat, long)

            YOUR_API_KEY = config('YOUR_API_KEY')


            gmaps = googlemaps.Client(key=YOUR_API_KEY)



            directions_result = gmaps.directions(start_location, end_location,mode="driving", alternatives=True)

            location_obj = Location.objects.all()
            fixed_locations = []

            for data in location_obj:
                location_dict = {
                    "lat": data.latitude,
                    "lng": data.longitude,
                    "title": data.address,

                    "location_id": data.id
                }
                fixed_locations.append(location_dict)
            fixed_locations.append({"lat": lat, "lng": long, 'title': "Me"})
            print("fixed_locations", fixed_locations)
            #
            # fixed_locations = [
            #
            #     {"lat": lat, "lng": long, 'title': "Me"},
            #     {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird"},
            #     {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri"},
            #     {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace"}
            # ]

            return render(request, 'direction.html',
                          {'directions': directions_result[0]['legs'][0]['steps'], 'fixed_locations': fixed_locations,'google_maps_api_key': YOUR_API_KEY})
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template direction.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)


class AllLocationGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """


    def get(self, request):
        """
        Geocode the given address
        """
        try:
            print("Inside: first *****", self.__class__.__name__)
            print("Request params: ", request)
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)
            user.current_location = True
            user.save()



            address = request.GET.get('address')
            print("address", address)

            latitude = (request.GET.get('latitude'))
            longitude = (request.GET.get('longitude'))

            print("type of latitude", type(latitude))
            print("type of longitude", type(longitude))

            lat = 0
            lon = 0
            try:
                lat = float(latitude)
                print("type a", lat)
                lon = float(longitude)
                print("type b", lon)
            except:
                print("in exception")


            if latitude and longitude:
                start_location = (latitude, longitude)

            YOUR_API_KEY = config('YOUR_API_KEY')

            gmaps = googlemaps.Client(key=YOUR_API_KEY)

            if address:

                geocode_result = gmaps.geocode(address)

                if geocode_result:
                    location = geocode_result[0]['geometry']['location']
                    lat = float(location['lat'])
                    lon = float(location['lng'])

                else:
                    print("Geocode result not found for the given address")

            location_obj = Location.objects.all()
            location_obj = Location.objects.all()
            fixed_locations = []

            for data in location_obj:
                location_dict = {
                    "lat": data.latitude,
                    "lng": data.longitude,
                    "title": data.address,

                    "location_id": data.id
                }
                fixed_locations.append(location_dict)
            fixed_locations.append({"lat": lat, "lng": lon, 'title': "Me"})

            # fixed_locations = [
            #     {"lat": lat, "lng": lon, 'title': "Me"},
            #     {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird", "location_id": 1},
            #     {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri", "location_id": 2},
            #     {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace", "location_id": 2}
            # ]
            context = { 'fixed_locations': fixed_locations}
            print("context", context)
            return render(request, 'all_location.html',
                          context )
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template all_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)


class CurrentLocation(APIView):
    def get(self, request):
        """
        Geocode the given address
        """
        try:
            print("Inside: ", self.__class__.__name__)
            print("Request params: ", request.query_params)
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)

            return render(request, 'current_location.html' )
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template current_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)

class ManualCurrentLocation(APIView):
        def get(self, request):
            """
            Geocode the given address
            """
            try:
                print("Inside: ", self.__class__.__name__)
                print("Request params: ", request.query_params)
                user_email = request.session.get('email')

                user = CustomUser.objects.get(email=user_email)

                return render(request, 'manual_current_location.html',
                              )
            except TemplateDoesNotExist:
                return JsonResponse(
                    {'message': 'Template not found', 'error': 'The template manual_current_location.html does not exist'},
                    status=404)
            except CustomUser.DoesNotExist:
                # If the user does not exist, you can handle it accordingly
                # For example, you might want to return an error response
                return JsonResponse(
                    {'message': 'User not found', 'error': 'User with the provided email does not exist'},
                    status=404)

