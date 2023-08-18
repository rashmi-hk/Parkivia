from django.contrib import admin

# Register your models here.
from django.contrib import messages,admin
from .models import CustomUser,Location,SlotDetail,SlotBooking,SlotDetailVariant
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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

admin.site.register(Location)
admin.site.register(SlotDetailVariant)
admin.site.register(SlotDetail)
admin.site.register(SlotBooking)

