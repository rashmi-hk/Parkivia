from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser,SlotDetail,Location
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

class StaffLocationAPIList(APIView):


    def get(self, request):
        print("Inside staff location get", request)
        print("Inside staff location get", request.data)
        try:
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)
            # User with the provided email doesn't exist

            if not user.is_authenticated:
                print("User not authenticated")
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                    status=status.HTTP_401_UNAUTHORIZED)

            location_detail = Location.objects.all()
            location_detail_list = []
            for location_data in location_detail:
                location_detail_dict = {"location_name": location_data.name,
                                    "location_id": location_data.id,
                                    }
                location_detail_list.append(location_detail_dict)

            context = {'location_detail_list': location_detail_list}
            print("context", context)
            return render(request, 'staff_location.html',context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template staff_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)



    def patch(self, request):

        try:
            print("staff patch request", request.data)
            print("staff patch request", request.data.get)
            location_data = request.data['location']
            location_obj = Location.objects.get(id=location_data)
            user = request.session.get('email')
            cust_obj = CustomUser.objects.get(email=user)
            cust_obj.parking_lot_location = location_obj
            cust_obj.save()

            return JsonResponse({'message': 'Staff location updated successfully'})

        except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Exception as e:

            print('Unexpected error occurred:', str(e))
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
