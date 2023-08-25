from rest_framework import serializers
from .models import CustomUser,SlotDetail, SlotDetailVariant
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def assign_groups(self, group_list):
        self.groups.set(group_list)

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        # Create the user instance with the hashed password
        user = CustomUser.objects.create(password=hashed_password, **validated_data)
        return user
# serializers.py


class SlotDetailVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDetailVariant
        fields = ['capacity', 'available_slots', 'vehicle_type', 'hourly_rate']


class SlotDetailSerializer(serializers.ModelSerializer):
    slot_variants = SlotDetailVariantSerializer(many=True)

    class Meta:
        model = SlotDetail
        fields = ['name', 'opening_hours', 'location', 'slot_variants']

    def create(self, validated_data):
        slot_variants_data = validated_data.pop('slot_variants', [])
        slot_detail = SlotDetail.objects.create(**validated_data)

        for variant_data in slot_variants_data:
            SlotDetailVariant.objects.create(slot=slot_detail, **variant_data)

        return slot_detail


