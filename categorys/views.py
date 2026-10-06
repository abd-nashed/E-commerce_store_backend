from django.shortcuts import get_object_or_404
from .serializer import CategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from account.permissions import IsAdminStoreRole
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Category
# Create your views here.

# للزوار
@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# للمسؤولين
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminStoreRole])
def add_category(request):
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        category = serializer.save()
        return Response(
            {
                "details": "done",
                "category": CategorySerializer(category).data,
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {"details": "error", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminStoreRole])
def delete_category(request,pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return Response({'details':'done delete'},status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated,IsAdminStoreRole])
def update_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    serializer = CategorySerializer(
        category,
        data=request.data,
        partial=(request.method == 'PATCH'),
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "details": "done",
                "category": CategorySerializer(category).data,
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {"details": "error", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )