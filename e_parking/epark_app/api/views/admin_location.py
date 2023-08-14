from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,Location
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template import TemplateDoesNotExist
from django.core.serializers import serialize

class AdminLocationAPIList(APIView):
    def is_superuser(self, user):
        return user.is_superuser


    def get(self, request):
        print("Inside location get", request)
        print("Inside location get", request.data)
        try:
            all_location_obj = Location.objects.all()
            resulting_list = []
            for data in all_location_obj:
                data_dict = {"name": data.name,
                             "address": data.address}

                resulting_list.append(data_dict)

            context = {'locations': resulting_list}
            print("context", context)
            return render(request, 'admin_location.html',context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template all_location.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside location post", request)
        print("Inside location post", request.data)
        try:
            if not request.user.is_authenticated:
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                    status=status.HTTP_401_UNAUTHORIZED)

            if not self.is_superuser(request.user):
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You do not have permission to access this resource'},
                    status=status.HTTP_403_FORBIDDEN)

            user = request.session.get('email')
            address = request.data["address"]
            name = request.data["name"]

            cust_obj = CustomUser.objects.get(email=user)
            new_location = Location()
            new_location.address = address
            new_location.name = name
            new_location.save()

            return JsonResponse(status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return JsonResponse({'message': 'User not found', 'error': 'User with the provided email does not exist'},
                                status=404)