from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode

from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from base64 import urlsafe_b64decode
from decouple import config

CustomUser = get_user_model()


class ResetPasswordView(APIView):

    success_message = 'Password reset link sent to your email.'
    email_subject = 'Password Reset'

    def get(self, request):
        print("inside template name",request)


        return render(request, 'staff_forgot_password.html')

    def post(self, request):
        print("Inside post of reset pasword", request)
        print("Inside post of reset pasword", request.data)
        email =  request.data['email']
        print("email", email)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'staff_login.html', {'error_message': 'Invalid credentials'})

        # Generate token for password reset
        token = default_token_generator.make_token(user)

        # Create reset link with token
        reset_link = request.build_absolute_uri(f'/reset-password/confirm/{token}/')



        subject = 'Reset Password Link'
        message = render_to_string('staff_password_reset_email.html', {'user': user, 'reset_link': reset_link})

        from_email = config('email_from')
        recipient_list = [email]

        print("*****", from_email, recipient_list)
        send_mail(subject, message, from_email, recipient_list)


        messages.success(request, self.success_message)
        return redirect('reset_password')


class ResetPasswordConfirmView(View):
    template_name = 'staff_password_reset.html'
    error_message = 'Invalid reset link.'
    success_message = 'Password has been reset successfully.'

    def get(self, request, token):
        try:
            print("inside get method ResetPasswordConfirmView")
            uidb64 = self.get_user_id_from_token(token)  # Get uidb64 from token
            pk = self.get_user_id_from_token(uidb64)


            print("pk", pk)
            user = CustomUser.objects.get(pk=pk)
            print("user", user)
        except (CustomUser.DoesNotExist, ValueError, OverflowError, UnicodeDecodeError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, self.template_name, {'token': token})

        messages.error(request, self.error_message)
        return redirect('staff_signin')

    def post(self, request, token):
        user = self.get_user_from_token(token)
        if user is not None:
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.success(request, self.success_message)
            return redirect('staff_signin')

        messages.error(request, self.error_message)
        return redirect('staff_signin')

    def get_user_id_from_token(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
            print("user", user)
            return uid
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError:", e)
            print("Unable to decode bytes to Unicode")
            return None
        except Exception as e:
            print("Exception:", e)
            print("Unable to get uid")
            return None

    def get_user_from_token(self, token):
        uid = self.get_user_id_from_token(token)
        try:
            user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            user = None
        return user
