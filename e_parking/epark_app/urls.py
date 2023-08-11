from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .api.views.home import HomeAPIList
from .api.views.geo_map import GMapsGeocoding,CurrentLocation,ManualCurrentLocation,AllLocationGeocoding

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', HomeAPIList.as_view() , name='home'),
    path('current_location', CurrentLocation.as_view() , name='current_location'),
    path('manuall_location', ManualCurrentLocation.as_view() , name='manuall_location'),
    path('all_location', AllLocationGeocoding.as_view() , name='all_location'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin_utility_logout/', LogoutView.as_view(next_page='admin_utility_login'), name='admin_utility_logout'),
    path('gmap', GMapsGeocoding.as_view(), name='gmap'),
    # path('verify_otp', VerifyOtpAPIList.as_view() , name='verify_otp'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_complete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

