from rest_framework import serializers
from .models import Order, OrderItem


# ============ OrderItem ============

class OrderItemSerializer(serializers.ModelSerializer):
    """للعرض (Read)"""
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'product_price',
            'store_name',
            'quantity',
            'subtotal',
        ]
        read_only_fields = ['id', 'subtotal']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """للإضافة (Write)"""

    class Meta:
        model = OrderItem
        fields = [
            'product_id',
            'product_name',
            'product_price',
            'store_name',
            'quantity',
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('الكمية يجب أن تكون 1 على الأقل')
        return value

    def validate_product_price(self, value):
        if value < 0:
            raise serializers.ValidationError('السعر لا يمكن أن يكون سالبًا')
        return value


# ============ Order ============

class OrderSerializer(serializers.ModelSerializer):
    """للعرض (Read) — مع المنتجات"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'full_name',
            'phone',
            'address',
            'tracking_code',
            'status',
            'status_display',
            'total',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 'tracking_code', 'total',
            'created_at', 'updated_at', 'status_display',
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """للإضافة (Write) — مع المنتجات"""
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'full_name',
            'phone',
            'address',
            'items',
        ]

    def validate_full_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('الاسم قصير جدًا')
        return value.strip()

    def validate_phone(self, value):
        phone = value.strip()
        if len(phone) < 8:
            raise serializers.ValidationError('رقم الهاتف غير صالح')
        return phone

    def validate_address(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('العنوان قصير جدًا')
        return value.strip()

    def validate_items(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('يجب إضافة منتج واحد على الأقل')
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # ⭐ حساب الإجمالي
        total = sum(
            item['product_price'] * item['quantity']
            for item in items_data
        )

        # ⭐ إنشاء الطلب
        order = Order.objects.create(
            total=total,
            **validated_data
        )

        # ⭐ إنشاء المنتجات
        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order