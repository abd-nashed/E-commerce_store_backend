from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """للعرض (Read) — مع كل الحقول"""

    class Meta:
        model = ContactMessage
        fields = [
            'id', 'full_name', 'phone', 'message',
             'created_at',
        ]
        read_only_fields = ['id', 'is_read', 'created_at']


class ContactCreateSerializer(serializers.ModelSerializer):
    """للإرسال (Write) — بدون id و is_read"""

    class Meta:
        model = ContactMessage
        fields = ['full_name', 'phone', 'message']

    def validate_full_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('الاسم قصير جدًا (3 أحرف على الأقل)')
        return value.strip()

    def validate_phone(self, value):
        phone = value.strip()
        if len(phone) < 8:
            raise serializers.ValidationError('رقم الهاتف غير صالح')
        return phone