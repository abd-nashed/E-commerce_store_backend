from rest_framework import serializers
from .models import Store, StoreRequest


# ============ Store ============

class StoreSerializer(serializers.ModelSerializer):
    """للعرض (Read)"""

    class Meta:
        model = Store
        fields = [
            'id', 'name', 'phone', 'description',
            'region', 'image', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class StoreCreateSerializer(serializers.ModelSerializer):
    """للإضافة/التعديل (Write)"""

    class Meta:
        model = Store
        fields = ['name', 'phone', 'description', 'region', 'image']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('اسم المتجر قصير جدًا')
        return value.strip()

    def validate_phone(self, value):
        phone = value.strip()
        if len(phone) < 8:
            raise serializers.ValidationError('رقم الهاتف غير صالح')
        return phone

    def validate_description(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('الوصف قصير جدًا')
        return value.strip()


# ============ StoreRequest ============

class StoreRequestSerializer(serializers.ModelSerializer):
    """للعرض (Read)"""

    class Meta:
        model = StoreRequest
        fields = [
            'id', 'store_name', 'phone', 'description',
            'region', 'image', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class StoreRequestCreateSerializer(serializers.ModelSerializer):
    """للإرسال (Write) — من الزوار"""

    class Meta:
        model = StoreRequest
        fields = ['store_name', 'phone', 'description', 'region', 'image']

    def validate_store_name(self, value):
        name = value.strip()

        if len(name) < 3:
            raise serializers.ValidationError('اسم المتجر قصير جدًا')

        if Store.objects.filter(name=name).exists():
            raise serializers.ValidationError('هذا الاسم مستخدم بالفعل')

        if StoreRequest.objects.filter(store_name=name).exists():
            raise serializers.ValidationError('يوجد طلب سابق بنفس الاسم')

        return name

    def validate_phone(self, value):
        phone = value.strip()
        if len(phone) < 8:
            raise serializers.ValidationError('رقم الهاتف غير صالح')
        return phone

    def validate_description(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('الوصف قصير جدًا')
        return value.strip()