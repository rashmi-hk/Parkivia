
import logging
import googlemaps
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import geocoder
from decouple import config

LOGGER = logging.getLogger(__name__)


class GMapsGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """

    def get(self, request):
        """
        Geocode the given address
        """
        print("Inside: first *****", self.__class__.__name__)
        print("Request params: ", request)



        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        current_latitude = request.GET.get('current_lat')
        current_longitude = request.GET.get('current_lng')
        print("***********", latitude,longitude)
        travling_mode =  request.GET.get('travelmode')
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


        fixed_locations = [

            {"lat": lat, "lng": long, 'title': "Me"},
            {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird"},
            {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri"},
            {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace"}
        ]

        return render(request, 'direction.html',
                      {'directions': directions_result[0]['legs'][0]['steps'], 'fixed_locations': fixed_locations,'google_maps_api_key': YOUR_API_KEY,'travling_mode':travling_mode})


class AllLocationGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """

    # def get_current_location(self):
    #     url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={'AIzaSyBgytWbW7G8sUUXvUfYpPG6dJS4N5M4WQw'}"
    #     response = requests.post(url)
    #
    #     if response.status_code == 200:
    #         location_data = response.json()
    #         latitude = location_data['location']['lat']
    #         longitude = location_data['location']['lng']
    #         return latitude, longitude
    #     else:
    #         return None

    def get(self, request):
        """
        Geocode the given address
        """
        print("Inside: first *****", self.__class__.__name__)
        print("Request params: ", request)

        start_location = request.GET.get('address')
        print("start_location", start_location)

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
        # print("***********", type(latitude), type(longitude))
        # current_location = self.get_current_location()
        # print("current_location", current_location)

        if latitude and longitude:
            start_location = (latitude, longitude)

        YOUR_API_KEY = config('YOUR_API_KEY')

        gmaps = googlemaps.Client(key=YOUR_API_KEY)

        end_location = 'balamuri, Mysore'
        # directions_result = gmaps.directions(start_location, end_location, mode="driving", alternatives=True)

        fixed_locations = [
            {"lat": lat, "lng": lon, 'title': "Me"},
            {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird", "location_id": 1},
            {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri", "location_id": 2},
            {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace", "location_id": 2}
        ]
        context = { 'fixed_locations': fixed_locations}
        print("context", context)
        return render(request, 'all_location.html',
                      context )


class CurrentLocation(APIView):
    def get(self, request):
        """
        Geocode the given address
        """
        print("Inside: ", self.__class__.__name__)
        print("Request params: ", request.query_params)

        return render(request, 'current_location.html',
                     )

class ManualCurrentLocation(APIView):
        def get(self, request):
            """
            Geocode the given address
            """
            print("Inside: ", self.__class__.__name__)
            print("Request params: ", request.query_params)

            return render(request, 'manual_current_location.html',
                          )

