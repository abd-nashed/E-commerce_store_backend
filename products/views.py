from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializer import ProductSerializer, ProductCreateSerializer
from account.permissions import IsAdminStoreRole


#  للزوار

@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk, is_active=True)
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_by_store(request, store_id):
    """⭐ منتجات متجر معين"""
    products = Product.objects.filter(store_id=store_id, is_active=True)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

#  للمسؤولين

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def add_product(request):
    serializer = ProductCreateSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save()
        return Response(
            {
                'details': 'تم إنشاء المنتج بنجاح',
                'product': ProductSerializer(product, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductCreateSerializer(
        product,
        data=request.data,
        partial=True,
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'details': 'تم تحديث المنتج بنجاح',
                'product': ProductSerializer(product, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {'details': 'error', 'errors': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminStoreRole])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return Response(
        {'details': 'تم حذف المنتج بنجاح'},
        status=status.HTTP_204_NO_CONTENT,
    )