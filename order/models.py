from django.db import models
import uuid


class Order(models.Model):
    """⭐ طلب الزبون"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'لم يتم الإرسال بعد'
        SHIPPED = 'shipped', 'في طريقه إليك'
        DELIVERED = 'delivered', 'تم البيع'
        CANCELLED = 'cancelled', 'ملغي'

    full_name = models.CharField(max_length=200, verbose_name='اسم الزبون')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    address = models.TextField(verbose_name='الموقع / العنوان')

    tracking_code = models.CharField(
        max_length=12, unique=True, blank=True, verbose_name='كود التتبع'
    )

    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.PENDING, verbose_name='حالة الطلب'
    )

    total = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='الإجمالي'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'

    def __str__(self):
        return f"طلب #{self.id} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """⭐ منتج داخل الطلب"""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='الطلب'
    )

    product_id = models.PositiveIntegerField(verbose_name='رقم المنتج')
    product_name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='سعر المنتج'
    )
    store_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='اسم المتجر'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'منتج في الطلب'
        verbose_name_plural = 'منتجات الطلبات'

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.product_price * self.quantity


class DailySales(models.Model):
    """⭐ سجل المبيعات اليومية (لا يتأثر بحذف الطلبات)"""

    date = models.DateField(
        unique=True,
        verbose_name='التاريخ'
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='إجمالي المبيعات'
    )
    orders_count = models.PositiveIntegerField(
        default=0, verbose_name='عدد الطلبات'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'مبيعات يومية'
        verbose_name_plural = 'المبيعات اليومية'

    def __str__(self):
        return f"{self.date} - {self.total}"