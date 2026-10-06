from django.shortcuts import get_object_or_404
from .serializer import AddUserSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .permissions import IsAdminRole


# ============ إدارة المستخدمين (superadmin فقط) ============

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminRole])
def add_user(request):
    serializer = AddUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {'details': 'done add user', 'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminRole])
def delete_user(request, pk):
    user = get_object_or_404(User, id=pk)

    # 1. لا تحذف نفسك
    if request.user.id == user.id:
        return Response(
            {'error': 'لا يمكنك حذف حسابك الخاص'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. لا تحذف مدير عام آخر
    if user.role == 'superadmin':
        return Response(
            {'error': 'لا يمكنك حذف مدير عام آخر'},
            status=status.HTTP_403_FORBIDDEN
        )

    user.delete()

    return Response(
        {'details': 'done delete'},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminRole])
def get_users(request):
    users = User.objects.all().order_by('-date_joined')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ============ تسجيل الدخول (كل الأدوار) ============

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def verify_superadmin(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    if not username or not password:
        return Response(
            {'error': 'الاسم وكلمة المرور مطلوبان'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # ⭐ نشفّر كلمة مرور وهمية لنأخذ نفس الوقت
        make_password(password)
        return Response({'error': 'بيانات الدخول غير صحيحة'}, 401)

    if not user.check_password(password):
        return Response(
            {'error': 'بيانات الدخول غير صحيحة'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'هذا الحساب معطّل'},
            status=status.HTTP_403_FORBIDDEN
        )

    # ⭐ يقبل كل الأدوار
    allowed_roles = ['superadmin', 'admin', 'store', 'sales']
    if user.role not in allowed_roles:
        return Response(
            {'error': 'لا يمكنك الدخول'},
            status=status.HTTP_403_FORBIDDEN
        )

    # ⭐ إنشاء التوكن
    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'username': user.username,
        'role': user.role,
        'isSuperAdmin': user.role == 'superadmin',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_200_OK)


# ============ التحقق الدوري ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_me(request):
    try:
        user = User.objects.get(id=request.user.id)
        if not user.is_active:
            return Response(
                {'error': 'الحساب معطّل'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({
            'success': True,
            'username': user.username,
            'role': user.role,
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'المستخدم غير موجود'},
            status=status.HTTP_401_UNAUTHORIZED
        )