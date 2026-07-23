from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


# ─── Products ───────────────────────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class ProductListView(APIView):
    """GET all products / POST create a product."""
    permission_classes = []

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'created', 'id': serializer.instance.pk},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'status': 'error', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailView(APIView):
    """GET / PUT (partial) / DELETE a single product."""
    permission_classes = []

    def _get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self._get_object(pk)
        if product is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        product = self._get_object(pk)
        if product is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'updated'})
        return Response(
            {'status': 'error', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        product = self._get_object(pk)
        if product is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'status': 'deleted'})


# ─── Orders ─────────────────────────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class OrderListView(APIView):
    """GET all orders / POST create an order."""
    permission_classes = []

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'created', 'id': serializer.instance.pk},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'status': 'error', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailView(APIView):
    """GET / PUT (partial) / DELETE a single order."""
    permission_classes = []

    def _get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self._get_object(pk)
        if order is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order).data)

    def put(self, request, pk):
        order = self._get_object(pk)
        if order is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'updated'})
        return Response(
            {'status': 'error', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        order = self._get_object(pk)
        if order is None:
            return Response({'status': 'not_found'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response({'status': 'deleted'})
