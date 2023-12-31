from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
from django.utils.crypto import get_random_string
from django.template import TemplateDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password


class UserSignInAPIList(APIView):

    def get(self, request):
        try:
            print("Inside user signin")
            return render(request, 'user_login.html')
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template user_login.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside user post", request)
        print("Inside user  post", request.data)
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


            if not password_matched:
                print("invalid")

                return render(request, 'user_login.html', {'error_message': 'Invalid credentials'})

            elif customer.is_staff or customer.is_superuser:
                print("Invalid")
                return render(request, 'user_login.html', {'error_message': 'You do not have permission to log in.'})
            else:
                print("valid")
                request.session['customer_id'] = customer.id
                request.session['email'] = email

                return redirect('all_location')

        except CustomUser.DoesNotExist:
            # If the user does not exist, you can handle it accordingly
            # For example, you might want to return an error response
            return render(request, 'user_login.html', {'error_message': 'User not found'})