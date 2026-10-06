from django.db import models


class ContactMessage(models.Model):
    """رسائل الزوار عبر صفحة تواصل معنا"""

    full_name = models.CharField(
        max_length=200,
        verbose_name='الاسم الكامل'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف'
    )
    message = models.TextField(
        verbose_name='الرسالة'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='التاريخ والوقت'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'

    def __str__(self):
        return f"{self.full_name} - {self.phone}"