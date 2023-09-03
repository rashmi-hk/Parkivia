from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
# from ...models import
# import os
# from ...serializers import CartSerializer
# from django.core import serializers

from django.shortcuts import get_object_or_404
import json
import logging

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class HomeAPIList(APIView):

    def get(self,request):
        try:

            print("Inside get homeapi")
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)

            return render(request, 'staff_home.html')
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            print("Error:", e)
            return render(request, 'staff_home.html', {'errors': str(e)})