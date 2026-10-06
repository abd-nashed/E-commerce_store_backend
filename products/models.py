from django.db import models
from categorys.models import Category
from stores.models import Store   # ⭐ جديد


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    # ⭐ الصورة الرئيسية
    main_image = models.ImageField(
        upload_to='products/main/',
        blank=True,
        null=True,
        verbose_name='الصورة الرئيسية'
    )

    # ⭐ 5 صور إضافية
    image_1 = models.ImageField(
        upload_to='products/gallery/',
        blank=True, null=True,
        verbose_name='صورة إضافية 1'
    )
    image_2 = models.ImageField(
        upload_to='products/gallery/',
        blank=True, null=True,
        verbose_name='صورة إضافية 2'
    )
    image_3 = models.ImageField(
        upload_to='products/gallery/',
        blank=True, null=True,
        verbose_name='صورة إضافية 3'
    )
    image_4 = models.ImageField(
        upload_to='products/gallery/',
        blank=True, null=True,
        verbose_name='صورة إضافية 4'
    )
    image_5 = models.ImageField(
        upload_to='products/gallery/',
        blank=True, null=True,
        verbose_name='صورة إضافية 5'
    )

    # ⭐ القسم
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='القسم'
    )

    # ⭐⭐ المتجر — اختياري
    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='المتجر'
    )

    # ⭐ هل عليه خصم؟
    has_discount = models.BooleanField(
        default=False,
        verbose_name='يوجد خصم؟'
    )

    # ⭐ نسبة الخصم
    discount_percent = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='نسبة الخصم (%)'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.has_discount and self.discount_percent:
            discount = (self.price * self.discount_percent) / 100
            return round(self.price - discount, 2)
        return self.price

    @property
    def all_images(self):
        imgs = [self.main_image]
        for img in [self.image_1, self.image_2, self.image_3, self.image_4, self.image_5]:
            if img:
                imgs.append(img)
        return imgs