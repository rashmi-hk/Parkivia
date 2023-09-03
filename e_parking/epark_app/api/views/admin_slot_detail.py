from rest_framework.views import APIView
from django.shortcuts import render, redirect
import json
from ...models import CustomUser,Location, SlotDetail, SlotDetailVariant
from ...serializers import SlotDetailSerializer,SlotDetailVariantSerializer
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
from django.db.models import Q
import ast
from decimal import Decimal

class AdminGetSlotDetailAPIList(APIView):

        def get(self, request):
            try:
                print("Inside get AdminGetSlotDetailAPIList", request)
                user_email = request.session.get('email')
                print("user_email", user_email)
                user = CustomUser.objects.get(email=user_email)

                location  = request.GET.get('location_id')
                print("location", location)
                location_obj = Location.objects.get(id=location)
                slot_detail_obj = SlotDetail.objects.filter(location=location)
                print("slot_detail_obj", slot_detail_obj)
                resulting_list = []
                for data in slot_detail_obj:
                    result_var_list = []
                    slot_variant_obj = SlotDetailVariant.objects.filter(slot__id=data.id)
                    for var_data in slot_variant_obj:
                        var_dict = {"capacity": var_data.capacity,
                            "available_slots": var_data.available_slots,
                            "vehicle_type": var_data.vehicle_type,
                             "hourly_rate_1_hour" : var_data.hourly_rate_1_hour,
                             "hourly_rate_3_hours" : var_data.hourly_rate_3_hours,
                            "hourly_rate_6_hours" : var_data.hourly_rate_6_hours,
                            "hourly_rate_12_hours" : var_data.hourly_rate_12_hours,
                            "daily_rate" : var_data.daily_rate
                             }

                        result_var_list.append(var_dict)

                    resulting_dict = {
                        "slot_detail_id":data.id,
                        "name": data.name,
                        "location": data.location,
                        "variant_data": result_var_list


                    }
                    resulting_list.append(resulting_dict)
                context = {"resulting_list" : resulting_list,
                           "slot_location": location_obj.name}
                print("context", context)
                return render(request, 'admin_get_slot_detail.html', context)
            except TemplateDoesNotExist:
                return JsonResponse(
                    {'message': 'Template not found',
                     'error': 'The template admin_get_slot_detail.html does not exist'},
                    status=404)
            except CustomUser.DoesNotExist:
                return JsonResponse(
                    {'message': 'User not found', 'error': 'User not found'},
                    status=404)


        def patch(self, request):

            try:
                print(" PATCH admin slot detail request", request)
                print(" patch admin slot detail  request", request.data)
                user_email = request.session.get('email')
                print("user_email", user_email)
                user = CustomUser.objects.get(email=user_email)

                slot_detail_id = request.data["slot_detail_id"]
                name = request.data["name"]
                location = request.data["location"]
                slot_variants = request.data["slot_variants"]
                print("slot_variants", slot_variants)

                slot_obj = None
                try:
                    if slot_detail_id:
                        location_obj = Location.objects.get(id=location)

                        slot_obj = SlotDetail.objects.get(
                            Q(id=slot_detail_id) & Q(name__iexact=name) & Q(
                                location=location_obj)
                        )
                        print("This slotdetail data already present no need to edit", slot_obj)
                except:
                    print("SlotDetail Editing is done")
                    location_obj = Location.objects.get(id=location)
                    slot_obj = SlotDetail.objects.get(id=slot_detail_id)
                    slot_obj.name = name
                    slot_obj.location = location_obj
                    slot_obj.save()

                for var_data in slot_variants:
                    print("var_data", var_data)
                    capacity = var_data["capacity"]
                    available_slots = var_data["available_slots"]
                    vehicle_type = var_data["vehicle_type"]
                    hourly_rate_1_hours = var_data["hourly_rate_1_hour"]
                    hourly_rate_3_hours = var_data["hourly_rate_3_hours"]
                    hourly_rate_6_hours = var_data["hourly_rate_6_hours"]
                    hourly_rate_12_hours = var_data["hourly_rate_12_hours"]
                    daily_rate = var_data["daily_rate"]


                    var_slot_data_id = var_data["var_slot_id"]
                    try:
                        print("var_slot_data_id", var_slot_data_id)
                        print("var_slot_data_id length ", len(var_slot_data_id))
                        if var_slot_data_id:

                            exist_data_slot = SlotDetailVariant.objects.get(
                                id=var_slot_data_id,
                                slot=slot_obj,
                                capacity=capacity,
                                available_slots=available_slots,
                                vehicle_type__iexact=vehicle_type,
                                hourly_rate_1_hour = hourly_rate_1_hours,
                                hourly_rate_3_hour = hourly_rate_3_hours,
                                hourly_rate_6_hour = hourly_rate_6_hours,
                                hourly_rate_12_hour = hourly_rate_12_hours,
                                daily_rate = daily_rate
                            )

                            print("This SlotDetailVariant data already present no need to edit")
                        else:
                            # Create new SlotDetailVariant
                            print("id not exist")
                            if (
                                    len(capacity) == 0
                                    or len(vehicle_type) == 0
                                    or len(hourly_rate_1_hours) == 0
                                    or len(hourly_rate_3_hours) == 0
                                    or len(hourly_rate_6_hours) == 0
                                    or len(hourly_rate_12_hours) == 0
                                    or len(daily_rate) == 0
                            ):
                                return JsonResponse(
                                    {"error": "Required fields are missing in the variant data"},
                                    status=400,  # Bad Request
                                )

                            if vehicle_type != '':
                                print("available_slots", available_slots)
                                if len(available_slots)==0:
                                    available_slots = 0
                                new_variant_obj = SlotDetailVariant.objects.create(
                                    slot=slot_obj,
                                    capacity=capacity,
                                    available_slots=available_slots,
                                    vehicle_type=vehicle_type,
                                    hourly_rate_1_hour=hourly_rate_1_hours,
                                    hourly_rate_3_hours=hourly_rate_3_hours,
                                    hourly_rate_6_hours=hourly_rate_6_hours,
                                    hourly_rate_12_hours=hourly_rate_12_hours,
                                    daily_rate=daily_rate
                                )
                                print("Created new SlotDetailVariant:", new_variant_obj)


                    except:

                        print("SlotDetailVariant Editing is done")
                        slot_var_obj = SlotDetailVariant.objects.get(id=var_slot_data_id)
                        slot_var_obj.capacity = capacity
                        slot_var_obj.available_slots = available_slots
                        slot_var_obj.vehicle_type = vehicle_type
                        slot_var_obj.hourly_rate_1_hour = hourly_rate_1_hours
                        slot_var_obj.hourly_rate_3_hours = hourly_rate_3_hours
                        slot_var_obj.hourly_rate_6_hours = hourly_rate_6_hours
                        slot_var_obj.hourly_rate_12_hours = hourly_rate_12_hours
                        slot_var_obj.daily_rate = daily_rate
                        slot_var_obj.save()

                print("Saved sucess")
                return JsonResponse({'message': 'SlotDetail updated successfully'}, status=status.HTTP_201_CREATED)


            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'}, status=404)
            except Exception as e:

                print('Unexpected error occurred:', str(e))
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

class AdminEditSlotDetailAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get AdminEditSlotDetailAPIList", request)
            user_email = request.session.get('email')
            print("user_email", user_email)
            user = CustomUser.objects.get(email=user_email)


            slot_detail_id = request.GET.get('slot_id')
            print("slot_detail_id", slot_detail_id)
            print("slot_detail_id", type(slot_detail_id))
            name = request.GET.get('name')
            slot_id = slot_detail_id

            all_location = Location.objects.all()

            slot_data_obj = SlotDetail.objects.get(id = slot_id)
            print("slot_data_obj get data obj ", slot_data_obj)
            slot_variant_obj = SlotDetailVariant.objects.filter(slot__id=slot_data_obj.id)
            print("slot_variant_obj variant",slot_variant_obj )
            vehicle_choices = CustomUser.VEHICLE_CHOICES

            existing_vehicle_types = set()
            for variant in slot_variant_obj:
                existing_vehicle_types.add(variant.vehicle_type)

            print("slot_detail_id", slot_detail_id)

            var_list = []
            for var_data in slot_variant_obj:
               var_dict = { "slot" : var_data.slot,
                            "var_slot_id": var_data.id,
                            "capacity": var_data.capacity,
                            "available_slots": var_data.available_slots,
                            "vehicle_type": var_data.vehicle_type,
                            "hourly_rate_1_hour": var_data.hourly_rate_1_hour,
                            "hourly_rate_3_hours": var_data.hourly_rate_3_hours,
                            "hourly_rate_6_hours": var_data.hourly_rate_6_hours,
                            "hourly_rate_12_hours": var_data.hourly_rate_12_hours,
                            "daily_rate": var_data.daily_rate

                            }


               var_list.append(var_dict)
            print("var_list  add data to list")
            filtered_vehicle_choices = [(choice_value, choice_label) for choice_value, choice_label in vehicle_choices
                                        if choice_value not in existing_vehicle_types]
            print(" filtered_vehicle_choices ",  filtered_vehicle_choices )

            context = {
                'slot_detail_id': slot_detail_id,
                'name': slot_data_obj.name,
                'location': all_location,
                "slot_location":slot_data_obj.location,
                'slot_variants':var_list,
                "vehicle_choices": filtered_vehicle_choices,
                "slot_location_id": slot_data_obj.location
            }


            print("context", context)
            print("Edited sucess")
            return render(request, 'admin_edit_slot_detail.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found',
                 'error': 'The template admin_edit_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)




    def delete(self, request):

        print("inside delete slotvariant item", request.data)
        print("inside delete slotdetail ", request)


        variant_id =  request.data.get('variant_id')
        print("variant_id", variant_id)
        slot_detail_id =  request.GET.get('slot_detail_id')



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
            if variant_id:
                print("Inside variant delete")
                variant = SlotDetailVariant.objects.get(id=variant_id)
                variant.delete()
                print("Delete sucessfully")
                return HttpResponse("SlotDetailVariant deleted successfully.")
            else:
                print("Inside slot delete")
                slot_detail = SlotDetail.objects.get(id=slot_detail_id)
                slot_detail.delete()
                print("Delete sucessfully")
                return HttpResponse("SlotDetail deleted successfully.")

        except SlotDetail.DoesNotExist:
            return HttpResponseBadRequest("SlotDetail not found.")
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

class AddSlotDetailAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get AddSlotDetailAPIList", request)
            user_email = request.session.get('email')
            print("user_email", user_email)
            user = CustomUser.objects.get(email=user_email)

            location_id = request.GET.get("location_id")
            all_location = Location.objects.filter(id=location_id)
            context = {}
            if all_location.exists():
                location = all_location.first()
                print("location", location)# Assuming you're interested in the first result

                context.update({"all_location":location})



            vehicle_choices = SlotDetailVariant.VEHICLE_CHOICES

            context.update({
                       "vehicle_choices": vehicle_choices})
            print("context", context)
            return render(request, 'admin_add_slot_detail.html', context)

        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found',
                 'error': 'The template admin_edit_location.html does not exist'},
                status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

    def post(self, request, format=None):
        print("Inside create ", request)
        print("Inside create ", request.data)
        try:
            user_email = request.session.get('email')
            print("user_email", user_email)
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

        name = request.data.get('name')

        location = request.data.get('location')
        slot_variants_data = json.loads(request.data.get('slot_variants'))


        print("slot_variants_data", slot_variants_data)


        if not name or not location or not slot_variants_data:
            print("Missing fields***********")
            return Response({'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        print("JIII")
        location_obj = Location.objects.get(id=location)
        exestence_check = None
        try:
            exestence_check = SlotDetail.objects.get( name=name,
                location=location_obj)

        except SlotDetail.DoesNotExist:
            print("SlotDetail not found.")

        if not exestence_check:
            print("Data not exist")
            slot_detail = SlotDetail.objects.create(
                name=name,
                location=location_obj
            )
            print("Created SlotDetail")
            slot_variants = []
            for variant_data in slot_variants_data:
                print("variant_data", variant_data)
                capacity = variant_data['capacity']

                vehicle_type = variant_data['vehicle_type']
                print("****ihkj")
                hourly_rate_1_hour = variant_data['hourly_rate_1_hour']
                print("HII")
                hourly_rate_3_hours = variant_data['hourly_rate_3_hours']
                hourly_rate_6_hours = variant_data['hourly_rate_6_hours']
                hourly_rate_12_hours = variant_data['hourly_rate_12_hours']
                daily_rate = variant_data['daily_rate']
                print("************",hourly_rate_1_hour,hourly_rate_3_hours,hourly_rate_6_hours,hourly_rate_12_hours,daily_rate)
                if capacity and  vehicle_type and hourly_rate_12_hours and hourly_rate_6_hours and hourly_rate_3_hours and hourly_rate_1_hour and daily_rate:
                    variant = SlotDetailVariant.objects.create(
                        slot=slot_detail,
                        capacity=capacity,
                        vehicle_type=vehicle_type,
                        hourly_rate_1_hour=hourly_rate_1_hour,
                        hourly_rate_3_hours = hourly_rate_3_hours,
                        hourly_rate_6_hours = hourly_rate_6_hours,
                        hourly_rate_12_hours = hourly_rate_12_hours,
                        daily_rate = daily_rate
                    )
                    print("Created")
                    slot_variants.append({
                        'capacity': capacity,
                        'vehicle_type': vehicle_type,
                         'hourly_rate_1_hour': hourly_rate_1_hour,
                        'hourly_rate_3_hours' : hourly_rate_3_hours,
                        'hourly_rate_6_hours' : hourly_rate_6_hours,
                        'hourly_rate_12_hours' : hourly_rate_12_hours
                    })

            response_data = {
                'slot_detail': {
                    'name': name,

                    'location': location
                },
                'slot_variants': slot_variants
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print("Data already exist")
            return Response({'message': 'data already exist'}, status=status.HTTP_400_BAD_REQUEST)