from django.db import models


class Store(models.Model):
    """⭐ المتاجر المُعتمدة"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='اسم المتجر'
    )
    phone = models.CharField(
    max_length=20,
    default='',
    verbose_name='رقم الهاتف'
   )
    description = models.TextField(
        verbose_name='الوصف'
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='المنطقة'
    )
    image = models.ImageField(
        upload_to='stores/',
        blank=True,
        null=True,
        verbose_name='صورة المتجر'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'متجر'
        verbose_name_plural = 'المتاجر'

    def __str__(self):
        return self.name


class StoreRequest(models.Model):
    """⭐ طلبات فتح متجر من الزوار"""

    store_name = models.CharField(
        max_length=200,
        verbose_name='اسم المتجر المطلوب'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='المنطقة'
    )
    image = models.ImageField(
        upload_to='store_requests/',
        blank=True,
        null=True,
        verbose_name='صورة المتجر'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الطلب'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'طلب متجر'
        verbose_name_plural = 'طلبات المتاجر'

    def __str__(self):
        return self.store_name