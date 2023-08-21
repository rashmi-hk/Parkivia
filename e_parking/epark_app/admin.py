from django.contrib import admin

# Register your models here.
from django.urls import path
from .api.views.admin_signup import AdminUtilityAPIList
from django.contrib import messages,admin
from .models import CustomUser,Location,SlotDetail,SlotBooking,SlotDetailVariant
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.shortcuts import render, redirect

from django import forms
from django.contrib.auth.admin import UserAdmin

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active','is_verified', 'address')}
            ),
        )

    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
# class LocationAdmin(admin.ModelAdmin):
#     # change_list_template = 'admin/admin_select_location.html'
#
#     # def get_urls(self):
#     #     urls = super().get_urls()
#     #     custom_urls = [
#     #         path('admin_custom/', self.admin_custom_view, name='admin_custom_view'),
#     #     ]
#     #     return custom_urls + urls
#
#     # @admin.site.admin_view
#     # def admin_custom_view(self, request):
#         # return render(request, 'admin/admin_select_location.html')
#
#     # Override the add_view method to use custom template for adding Location
#     def add_view(self, request, form_url='', extra_context=None):
#         self.change_form_template = 'admin/admin_select_location.html'
#         return super().add_view(request, form_url, extra_context)

admin.site.register(Location)


admin.site.register(SlotDetailVariant)
admin.site.register(SlotDetail)
admin.site.register(SlotBooking)

