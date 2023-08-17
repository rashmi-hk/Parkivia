from rest_framework.views import APIView
from django.shortcuts import render, redirect
from ...models import CustomUser
from django.core.mail import send_mail,EmailMultiAlternatives
from decouple import config
from django.utils.crypto import get_random_string
from django.template import TemplateDoesNotExist
from django.http import JsonResponse


class AdminUtilityAPIList(APIView):

    def get(self, request):
        try:
            print("Inside get homeapi")
            return render(request, 'admin_sign_up.html')
        except TemplateDoesNotExist:
            return JsonResponse(
                {'message': 'Template not found', 'error': 'The template admin_sign_up.html does not exist'},
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
                otp = otp

                check_existence = CustomUser.objects.filter(email=email).first()
                if not check_existence:
                    # Assuming 'user_dict' contains the necessary user information including 'email'
                    user = CustomUser.objects.create_user(username=username, email=email,
                                                          password=password, otp=otp, phone_number=phone_number,
                                                          address=address,
                                                          is_superuser=True,
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
                    return redirect('admin:login')
                else:
                    error_message = 'CustomUser with this email id already exist,Please try with different one'
                    return render(request, 'admin_sign_up.html', {'error_message': error_message})
        except  Exception as e:
            print(f"An unexpected error occurred: {e}")


