from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse


from django.shortcuts import get_object_or_404
import json
import logging

from django.http import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)

# Item api
class AdminHomeAPIList(APIView):

    def get(self,request):
        print("Inside admin get homeapi")
        try:
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)

            return render(request, 'admin_home.html')
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)

class AdminIdentity(APIView):
    def get(self, request):
        try:
            print("Inside admin get AdminIdentity")
            user_email = request.session.get('email')
            user = CustomUser.objects.get(email=user_email)

            return JsonResponse({"username": user.username})
        except CustomUser.DoesNotExist:
            return JsonResponse(
                {'message': 'User not found', 'error': 'User not found'},
                status=404)
