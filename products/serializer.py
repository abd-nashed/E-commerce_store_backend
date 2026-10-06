from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """⭐ للعرض (Read)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    store_name = serializers.CharField(     # ⭐ جديد
        source='store.name',
        read_only=True,
        allow_null=True
    )
    final_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description',
            'price', 'final_price',
            'stock',
            'main_image',
            'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
            'category', 'category_name',
            'store', 'store_name',     # ⭐ جديد
            'has_discount', 'discount_percent',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    """⭐ للإضافة/التعديل (Write)"""

    class Meta:
        model = Product
        fields = [
            'name', 'description',
            'price', 'stock',
            'main_image',
            'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
            'category',
            'store',                    # ⭐ جديد
            'has_discount', 'discount_percent',
            'is_active',
        ]

    def validate(self, data):
        # ⭐ الصورة الرئيسية إلزامية
        if not data.get('main_image') and not self.instance:
            raise serializers.ValidationError(
                {'main_image': 'الصورة الرئيسية مطلوبة'}
            )

        # ⭐ لو has_discount = True، لازم discount_percent
        if data.get('has_discount') and not data.get('discount_percent'):
            raise serializers.ValidationError(
                {'discount_percent': 'يجب تحديد نسبة الخصم'}
            )

        # ⭐ نسبة الخصم بين 1 و 99
        if data.get('has_discount'):
            percent = data.get('discount_percent')
            if percent and (percent < 1 or percent > 99):
                raise serializers.ValidationError(
                    {'discount_percent': 'نسبة الخصم يجب أن تكون بين 1 و 99'}
                )

        return data