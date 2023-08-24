from rest_framework import serializers
from .models import CustomUser,SlotDetail, SlotDetailVariant


class CustomUserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = CustomUser
        fields = "__all__"
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


