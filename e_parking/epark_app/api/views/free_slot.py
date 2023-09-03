from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser,SlotDetail,SlotDetailVariant,SlotBooking
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse


from django.shortcuts import get_object_or_404
import json
import logging
from rest_framework import status
from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class SlotFreeAPIList(APIView):

    def get(self,request):
        try:
            print("Inside SlotFreeAPIList", request)
            user_email = request.session.get('email')

            user = CustomUser.objects.get(email=user_email)
            # User with the provided email doesn't exist

            slot_id = request.GET.get('slot_id')
            vehicle_type = request.GET.get('vehicle_type')
            bookind_id = request.GET.get('bookind_id')
            if not user.is_authenticated:
                print("User not authenticated")
                return JsonResponse(
                    {'message': 'Unauthorized', 'error': 'You must be logged in to access this resource'},
                    status=status.HTTP_401_UNAUTHORIZED)

            slot_obj = SlotDetail.objects.get(id=slot_id)
            print("slot_obj", slot_obj)

            book_obj = SlotBooking.objects.get(id=bookind_id)
            book_obj.is_slot_relese = True
            book_obj.save()

            variants = SlotDetailVariant.objects.filter(slot__id=slot_obj.id, vehicle_type=vehicle_type)
            print("variants", variants)
            # Iterate through the variants and update available_slots
            for variant in variants:
                print("Inside for")
                variant.available_slots += 1
                variant.save()

            return JsonResponse({'message': 'Available slots updated successfully'}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

