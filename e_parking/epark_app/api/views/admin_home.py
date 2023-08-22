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
class AdminHomeAPIList(APIView):

    def get(self,request):
        print("Inside admin get homeapi")
        return render(request, 'admin_home.html')
        # return render(request, 'demo.html')