
import logging
import googlemaps
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import geocoder

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

        start_location = request.GET.get('address')
        print("start_location", start_location)

        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        print("***********", latitude,longitude)

        if latitude and longitude:
            start_location = (latitude, longitude)

        YOUR_API_KEY = "AIzaSyD7-wAJ3I-VlVGCWzDPVnjfwFgvqFgoM-M"


        gmaps = googlemaps.Client(key=YOUR_API_KEY)


        end_location = 'balamuri, Mysore'
        directions_result = gmaps.directions(start_location, end_location,mode="driving", alternatives=True)


        fixed_locations = [
            {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird"},
            {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri"},
            {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace"}
        ]

        return render(request, 'direction.html',
                      {'directions': directions_result[0]['legs'][0]['steps'], 'fixed_locations': fixed_locations})


class AllLocationGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """

    def get_current_location(self):
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={'AIzaSyD7-wAJ3I-VlVGCWzDPVnjfwFgvqFgoM-M'}"
        response = requests.post(url)

        if response.status_code == 200:
            location_data = response.json()
            latitude = location_data['location']['lat']
            longitude = location_data['location']['lng']
            return latitude, longitude
        else:
            return None

    def get(self, request):
        """
        Geocode the given address
        """
        print("Inside: first *****", self.__class__.__name__)
        print("Request params: ", request)

        start_location = request.GET.get('address')
        print("start_location", start_location)

        # latitude = (request.GET.get('latitude'))
        # longitude = (request.GET.get('longitude'))
        # print("***********", type(latitude), type(longitude))
        current_location = self.get_current_location()
        print("current_location", current_location)

        if current_location:
            start_location = (current_location[0], current_location[1])

        YOUR_API_KEY = "AIzaSyD7-wAJ3I-VlVGCWzDPVnjfwFgvqFgoM-M"

        gmaps = googlemaps.Client(key=YOUR_API_KEY)

        end_location = 'balamuri, Mysore'
        # directions_result = gmaps.directions(start_location, end_location, mode="driving", alternatives=True)

        fixed_locations = [
            {"lat": float(current_location[0]), "lng": float(current_location[1]), 'title': "Me"},
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

