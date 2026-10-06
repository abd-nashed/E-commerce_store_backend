from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Store, StoreRequest
from .serializer import (
    StoreSerializer,
    StoreCreateSerializer,
    StoreRequestSerializer,
    StoreRequestCreateSerializer,
)
from account.permissions import IsAdminAllRole, IsAdminStoreRole


# ============================================
#              Store — المتاجر
# ============================================

# ⭐ عرض كل المتاجر (للجميع)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_stores(request):
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ⭐ تفاصيل متجر واحد (للجميع)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    serializer = StoreSerializer(store, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ⭐ إضافة متجر (superadmin / admin / store)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def add_store(request):
    serializer = StoreCreateSerializer(data=request.data)

    if serializer.is_valid():
        store = serializer.save()
        return Response(
            {
                'details': 'تم إنشاء المتجر بنجاح',
                'store': StoreSerializer(store, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# ⭐ تعديل متجر (superadmin / admin / store)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def update_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    serializer = StoreCreateSerializer(
        store,
        data=request.data,
        partial=(request.method == 'PATCH'),
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'details': 'تم تعديل المتجر بنجاح',
                'store': StoreSerializer(store, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# ⭐ حذف متجر (superadmin / admin / store)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def delete_store(request, pk):
    store = get_object_or_404(Store, id=pk)
    store.delete()
    return Response(
        {'details': 'تم حذف المتجر بنجاح'},
        status=status.HTTP_204_NO_CONTENT,
    )


# ============================================
#          StoreRequest — طلبات المتاجر
# ============================================

# ⭐ عرض كل الطلبات (للمسؤولين)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def get_store_requests(request):
    requests = StoreRequest.objects.all()
    serializer = StoreRequestSerializer(requests, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ⭐ إرسال طلب (من أي شخص)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_store_request(request):
    serializer = StoreRequestCreateSerializer(data=request.data)

    if serializer.is_valid():
        store_request = serializer.save()
        return Response(
            {
                'details': 'تم إرسال طلبك بنجاح. سيتم مراجعته قريبًا.',
                'request': StoreRequestSerializer(store_request, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# ⭐ الموافقة على طلب (نقل من Requests إلى Stores)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def approve_store_request(request, pk):
    store_request = get_object_or_404(StoreRequest, id=pk)

    # ⭐ إنشاء المتجر من الطلب
    store = Store.objects.create(
        name=store_request.store_name,
        phone=store_request.phone,             # ⭐ جديد
        description=store_request.description,
        region=store_request.region,           # ⭐ جديد
        image=store_request.image,
    )

    # ⭐ حذف الطلب بعد النقل
    store_request.delete()

    return Response(
        {
            'details': 'تمت الموافقة على الطلب ونقل المتجر بنجاح',
            'store': StoreSerializer(store, context={'request': request}).data,
        },
        status=status.HTTP_201_CREATED,
    )


# ⭐ رفض طلب
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def reject_store_request(request, pk):
    store_request = get_object_or_404(StoreRequest, id=pk)
    store_request.delete()
    return Response(
        {'details': 'تم رفض الطلب'},
        status=status.HTTP_204_NO_CONTENT,
    )