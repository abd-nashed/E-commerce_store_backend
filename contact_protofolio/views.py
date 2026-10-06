# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .serializer import ContactMessageSerializer

@api_view(['POST'])
def contact_view(request):
    serializer = ContactMessageSerializer(data=request.data)

    if serializer.is_valid():
        # 1. حفظ في قاعدة البيانات
        instance = serializer.save()

        # 2. إرسال إلى Gmail
        try:
            send_mail(
                subject=f"رسالة جديدة: {instance.subject}",
                message=f"""
                من: {instance.name}
                الرقم: {instance.phone}

                الرسالة:
                {instance.message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['nashedabdalrzak@gmail.com'],  # بريدك
                fail_silently=False,
            )
            return Response(
                {"message": "تم إرسال الرسالة بنجاح"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"فشل الإرسال: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)