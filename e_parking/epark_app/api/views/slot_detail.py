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

class SlotDetailAPIList(APIView):


    def get(self, request):
        print("Inside location get", request)
        print("Inside location get", request.data)
        try:
            all_location_obj = SlotDetail.objects.all()
            resulting_list = []
            for data in all_location_obj:
                data_dict = {
                             "name": data.name,
                             "capacity": data.capacity,
                             "available_slots": data.available_slots,
                             "vehicle_type": data.vehicle_type,
                             "hourly_rate": data.hourly_rate,
                             "opening_hours": data.opening_hours,
                             "location": data.location}

                resulting_list.append(data_dict)

            context = {'slot_detail': resulting_list}
            print("context", context)
            return render(request, 'slot_detail.html',context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template slot_booking.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside location post", request)
        print("Inside location post user", request.user)
        print("Inside location post", request.data)
        try:
            user_email = request.session.get('email')


            user = CustomUser.objects.get(email=user_email)
           # User with the provided email doesn't exist


            if not user.is_authenticated:
                print("User not authenticated")
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                    status=status.HTTP_401_UNAUTHORIZED)

            if not self.is_superuser(user):
                print("user not superuser")
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You do not have permission to access this resource'},
                    status=status.HTTP_403_FORBIDDEN)

            print("User athenticated n superuser")
            address = request.data["address"]
            print("address", address)

            name = request.data["name"]
            print("name", name)


            new_location = Location()
            new_location.address = address
            new_location.name = name
            new_location.save()
            response_data = {'message': 'Request processed successfully'}
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)

    def delete(self, request):

        print("inside delete Location item", request.data)

        location_id = request.data['location_id']

        print("location_id", location_id)

        user_email = request.session.get('email')
        user = CustomUser.objects.get(email=user_email)

        if not user.is_authenticated:
            print("User not authenticated")
            return JsonResponse(
                {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                status=status.HTTP_401_UNAUTHORIZED)

        if not self.is_superuser(user):
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
