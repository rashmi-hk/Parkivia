from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import CustomUser, Location
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
from django.utils.crypto import get_random_string
from django.template import TemplateDoesNotExist
from django.http import JsonResponse


class StaffSignupAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get homeapi")
            location_detail = Location.objects.all()
            location_detail_list = []
            for location_data in location_detail:
                location_detail_dict = {"location_name": location_data.name,
                                        "location_id": location_data.id,
                                        }
                location_detail_list.append(location_detail_dict)

            context = {'location_detail_list': location_detail_list}
            print("context", context)
            return render(request, 'staff_sign_up.html', context)
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template staff_sign_up.html does not exist'},
                status=404)

    def post(self, request):
        print("Inside sign up post", request)
        print("Inside sign up", request.data)
        try:
            if request.data:
                print("****", request.data["username"])
                otp = get_random_string(length=6, allowed_chars='1234567890')
                password = request.data["password"]
                username = request.data["username"]
                email = request.data["email"]
                print("email ***", email)
                phone_number = request.data["phone_number"]
                address = request.data["address"]
                location_id = request.data["location"]
                location_obj = Location.objects.get(id=location_id)
                otp = otp

                check_existence = CustomUser.objects.filter(email=email).first()
                if not check_existence:
                    # Assuming 'user_dict' contains the necessary user information including 'email'
                    user = CustomUser.objects.create_user(username=username, email=email,
                                                          password=password, otp=otp, phone_number=phone_number,
                                                          address=address,
                                                          parking_lot_location=location_obj,
                                                          is_staff=True)

                    print("db save password", user.password)

                    # Send email with OTP
                    subject = 'Verify your email'
                    message = f'Your OTP is {otp}'
                    print("message", message)
                    from_email = config('email_from')
                    recipient_list = [email]

                    print("*****", from_email,recipient_list)
                    send_mail(subject, message, from_email, recipient_list)
                    # Redirect to verify page
                    context = {"email": email}
                    print("context", context)
                    context = {"email": email}
                    return render(request, 'staff_otp_verification.html', context)
                else:
                    error_message = 'CustomUser with this email id already exist,Please try with different one'
                    return render(request, 'staff_sign_up.html', {'error_message': error_message})
        except  Exception as e:
            print(f"An unexpected error occurred: {e}")


