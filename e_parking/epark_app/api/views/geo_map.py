
import logging
import googlemaps
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


LOGGER = logging.getLogger(__name__)


class GMapsGeocoding(APIView):
    """
    API wrapper for invoking google maps Geocoding API
    """



    def get(self, request):
        """
        Geocode the given address
        """
        print("Inside: ", self.__class__.__name__)
        print("Request params: ", request.query_params)


        YOUR_API_KEY = "AIzaSyASy6l6y7v2crnuY953tPgy0OcpHcxaf7c"


        gmaps = googlemaps.Client(key="AIzaSyCkrNAXjMGeM-HukizFu88BrgtU7DomJqI")
        print("************gmaps", gmaps)
        start_location = 'Dollarbird, Mysore'
        end_location = 'balamuri, Mysore'
        directions_result = gmaps.directions(start_location, end_location,mode="driving", alternatives=True)


        fixed_locations = [
            {"lat": 15.351132566178995, "lng": 75.11103627515064, 'title': "Dollarbird"},
            {"lat": 12.455558657572665, "lng": 75.94912661758033, 'title': "balamuri"},
            {"lat": 12.305225882078265, "lng": 76.65517489669053, 'title': "Mysore palace"}
        ]

        return render(request, 'direction.html',
                      {'directions': directions_result[0]['legs'][0]['steps'], 'fixed_locations': fixed_locations})

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

