from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import ContactMessage
from .serializer import ContactMessageSerializer, ContactCreateSerializer
from account.permissions import IsAllRole   # ⭐ أو IsSuperAdmin حسب عندك


# ============ للزوار: إرسال رسالة ============

@api_view(['POST'])
@permission_classes([AllowAny])
def send_message(request):
    """الزائر يُرسل رسالة"""
    serializer = ContactCreateSerializer(data=request.data)

    if serializer.is_valid():
        message = serializer.save()
        return Response(
            {
                'details': 'تم إرسال رسالتك بنجاح',
                'message': ContactMessageSerializer(message).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# ============ للمسؤولين: عرض/حذف الرسائل ============

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllRole])
def get_messages(request):
    """جلب كل الرسائل"""
    messages = ContactMessage.objects.all()
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllRole])
def delete_message(request, pk):
    """حذف رسالة"""
    message = get_object_or_404(ContactMessage, id=pk)
    message.delete()

    return Response(
        {'details': 'تم حذف الرسالة بنجاح'},
        status=status.HTTP_204_NO_CONTENT,
    )