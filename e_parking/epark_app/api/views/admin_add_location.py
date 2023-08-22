from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import CustomUser,Location
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

class AdminLocationAPIList(APIView):

    def get(self,request):
        try:
            print("Inside get AdminCustomAPIList")
            return render(request, 'admin_select_location.html')
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template admin_select_location.html does not exist'},
                status=404)



    def post(self, request):
        try:
            print("Inside post location ", request)
            print("Inside post location ", request.data)
            name = request.data["name"]
            address = request.data["address"]
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]

            try:
                user_email = request.session.get('email')
                user = CustomUser.objects.get(email=user_email)
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
            try:
                already_exist = Location.objects.get(name=name, address=address, latitude=latitude, longitude=longitude)
            except:
                already_exist = None

            if already_exist:
                return JsonResponse(
                    {'message': 'Data already exists', 'error': 'The provided data already exists'},
                    status=status.HTTP_409_CONFLICT
                )
            new_location = Location(name=name, address=address, latitude=latitude, longitude=longitude)
            new_location.save()
            print("Saved sucess")
            # Return a success response
            response_data = {'message': 'Request processed successfully'}
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)

        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User with the provided email does not exist'},
                status=404)
        except Exception as e:
            return Response(
                {'message': 'An error occurred', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdminGetLocationAPIList(APIView):

        def get(self, request):
            try:
                print("Inside get AdminEditLocationAPIList")
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
            except TemplateDoesNotExist:
                return JsonResponse(
                    {'message': 'Template not found',
                     'error': 'The template admin_get_location.html does not exist'},
                    status=404)


class AdminEditLocationAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get AdminEditLocationAPIList")
            address = request.GET.get('address')

            name = request.GET.get('name')
            latitude = request.GET.get('latitude')
            address = request.GET.get('address')
            longitude = request.GET.get('longitude')
            location_id = request.GET.get('location_id')

            context = {
                "location_id": location_id,
                "name": name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude
            }




            return render(request, 'admin_edit_location.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found',
                 'error': 'The template admin_edit_location.html does not exist'},
                status=404)

    def patch(self, request):

        try:
            print(" PATCH admin Location request", request)
            print(" patch admin location request", request.data)

            name = request.data["name"]
            address = request.data["address"]
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            location_id = request.data["location_id"]

            loc_obj = Location.objects.get(id=location_id)
            loc_obj.name = name
            loc_obj.latitude = latitude
            loc_obj.address = address
            loc_obj.longitude = longitude
            loc_obj.save()

            print("Saved sucess")
            return JsonResponse({'message': 'Staff location updated successfully'}, status=status.HTTP_201_CREATED)

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
