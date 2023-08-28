from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, F, Q
from ...models import CustomUser
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template import TemplateDoesNotExist


class StaffLoginAPIList(APIView):

    def get(self, request):

        try:
            print("request", request)
            return render(request, 'staff_login.html')
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template admin_login.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside home post", request)
        print("Inside home post", request.data)
        try:
            email = request.data['email']

            password = request.data['password']
            print("password type", type(password))
            customer = CustomUser.objects.get(email=email)  # Assuming User is the user model you are using
            print("customer", customer)
            print("password", customer.password)
            print("password type", type(customer.password))
            password_matched = check_password(password, customer.password)
            print("password_matched", password_matched)
            if password_matched and customer.is_staff and not customer.is_superuser:
                print("valid")
                request.session['customer_id'] = customer.id
                request.session['email'] = email

                return render(request, 'staff_home.html')
            else:
                print("invalid")

                return render(request, 'staff_login.html', {'error_message': 'Invalid credentials'})


        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return render(request, 'staff_login.html', {'error_message': 'User not found'})




