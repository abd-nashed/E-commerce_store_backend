from datetime import date, timedelta
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Order, DailySales
from .serializer import OrderSerializer, OrderCreateSerializer
from account.permissions import IsAdminSalesRole,IsAdminAllRole


# ============================================
#              للزوار
# ============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """⭐ إنشاء طلب جديد"""
    serializer = OrderCreateSerializer(data=request.data)

    if serializer.is_valid():
        order = serializer.save()
        return Response(
            {
                'details': 'تم إنشاء الطلب بنجاح',
                'order': OrderSerializer(order, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def track_order(request, code):
    """⭐ تتبع طلب بكود التتبع"""
    try:
        order = Order.objects.get(tracking_code=code.upper())
    except Order.DoesNotExist:
        return Response(
            {'error': 'كود التتبع غير صحيح'},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================
#              للمسؤولين
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminSalesRole])
def get_orders(request):
    """⭐ عرض كل الطلبات"""
    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminSalesRole])
def get_order(request, pk):
    """⭐ عرض طلب واحد"""
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminSalesRole])
def update_order_status(request, pk):
    """⭐ تعديل حالة الطلب + تسجيل المبيعات"""
    order = get_object_or_404(Order, id=pk)
    new_status = request.data.get('status')
    old_status = order.status

    valid = ['pending', 'shipped', 'delivered', 'cancelled']
    if new_status not in valid:
        return Response(
            {'error': 'حالة غير صالحة'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ⭐ عند التحويل إلى "تم البيع" → أضف للمبيعات اليومية
    if new_status == 'delivered' and old_status != 'delivered':
        today = date.today()
        daily, created = DailySales.objects.get_or_create(date=today)
        daily.total += order.total
        daily.orders_count += 1
        daily.save()

    # ⭐ عند إلغاء "تم البيع" → اخصم من المبيعات
    elif new_status != 'delivered' and old_status == 'delivered':
        today = date.today()
        try:
            daily = DailySales.objects.get(date=today)
            daily.total -= order.total
            daily.orders_count -= 1
            if daily.orders_count <= 0:
                daily.delete()
            else:
                daily.save()
        except DailySales.DoesNotExist:
            pass

    order.status = new_status
    order.save()

    return Response(
        {
            'details': 'تم تحديث الحالة',
            'order': OrderSerializer(order, context={'request': request}).data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminAllRole])
def delete_order(request, pk):
    """⭐ حذف طلب واحد"""
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response(
        {'details': 'تم حذف الطلب'},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminAllRole])
def delete_all_orders(request):
    """⭐ حذف كل الطلبات (superadmin + admin فقط)"""
    count = Order.objects.count()
    Order.objects.all().delete()

    return Response(
        {
            'details': f'تم حذف {count} طلب',
            'deleted_count': count,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminAllRole])
def get_daily_sales(request):
    """⭐ مبيعات آخر 7 أيام (من DailySales)"""
    today = date.today()
    seven_days_ago = today - timedelta(days=6)

    sales = DailySales.objects.filter(
        date__gte=seven_days_ago,
        date__lte=today,
    ).order_by('-date')

    data = [
        {
            'date': s.date,
            'total': float(s.total),
            'orders_count': s.orders_count,
        }
        for s in sales
    ]

    return Response(data, status=status.HTTP_200_OK)