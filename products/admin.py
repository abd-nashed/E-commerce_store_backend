from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'has_discount', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'has_discount', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active', 'has_discount']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'description', 'category')
        }),
        ('السعر والمخزون', {
            'fields': ('price', 'stock')
        }),
        ('الخصم', {
            'fields': ('has_discount', 'discount_percent'),
        }),
        ('⭐ الصور', {
            'fields': (
                'main_image',
                'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
            ),
            'description': '⭐ الصورة الرئيسية إلزامية. الباقي اختياري.'
        }),
        ('حالة المنتج', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )