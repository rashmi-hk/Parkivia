from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .api.views.staff_home import HomeAPIList
from .api.views.single_slot_detail import SingleSlotAPIList
from .api.views.slot_booking import SlotBookingAPIList,SlotBookingFormAPIList,SlotBookingEditAPIList
from .api.views.admin_signup import AdminUtilityAPIList
from .api.views.staff_signin import StaffLoginAPIList
from .api.views.staff_signup import StaffSignupAPIList
from .api.views.staff_verify_otp import StaffVerifyOtpAPIList
from .api.views.slot_detail import SlotDetailAPIList
from .api.views.staff_location import StaffLocationAPIList

from .api.views.geo_map import GMapsGeocoding,CurrentLocation,ManualCurrentLocation,AllLocationGeocoding
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse


from django.conf import settings
from django.conf.urls.static import static

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/forgot_password.html'

    def get_success_url(self):
        return reverse_lazy('admin_password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_sent.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset.html'

    def get_success_url(self):
        return reverse('admin_password_reset_complete')  # Replace with your desired URL name

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_done.html'



urlpatterns = [

    path('staff_home', HomeAPIList.as_view() , name='staff_home'),
    path('single_slot', SlotBookingFormAPIList.as_view() , name='single_slot'),
    path('single_slot_detail', SingleSlotAPIList.as_view() , name='single_slot_detail'),
    path('staff_location', StaffLocationAPIList.as_view() , name='staff_location'),
    path('edit_booking', SlotBookingEditAPIList.as_view() , name='edit_booking'),
    path('slot_detail', SlotDetailAPIList.as_view() , name='slot_detail'),
    path('admin_password_reset/', CustomPasswordResetView.as_view(), name='admin_password_reset'),
    path('admin_password_reset/done/', CustomPasswordResetDoneView.as_view(), name='admin_password_reset_done'),
    path('admin_reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
       name='admin_password_reset_confirm'),
    path('admin_reset/done/', CustomPasswordResetCompleteView.as_view(), name='admin_password_reset_complete'),

    path('slot_booking', SlotBookingAPIList.as_view() , name='slot_booking'),
    path('admin_signup', AdminUtilityAPIList.as_view() , name='admin_signup'),
    path('staff_signin', StaffLoginAPIList.as_view() , name='staff_signin'),
    path('staff_signup', StaffSignupAPIList.as_view() , name='staff_signup'),
    path('current_location', CurrentLocation.as_view() , name='current_location'),
    path('manuall_location', ManualCurrentLocation.as_view() , name='manuall_location'),
    path('all_location', AllLocationGeocoding.as_view() , name='all_location'),
    path('staff_verify_otp', StaffVerifyOtpAPIList.as_view(), name='staff_verify_otp'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_utility_logout/', LogoutView.as_view(next_page='admin_utility_login'), name='admin_utility_logout'),
    path('gmap', GMapsGeocoding.as_view(), name='gmap'),

    path('user_password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),name='user_password_reset'),
    path('user_password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='user_password_reset_done'),
    path('user_reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'),name='user_password_reset_confirm'),
    path('user_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='user_password_reset_complete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

