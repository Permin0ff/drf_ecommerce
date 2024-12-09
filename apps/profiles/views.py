from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsOwner
from apps.common.utils import set_dict_attr
from apps.profiles.models import ShippingAddress, Order, OrderItem
from apps.profiles.serializers import ProfileSerializer, ShippingAddressSerializer
from apps.shop.serializers import OrderSerializer, CheckItemSerializer, CheckItemOrderSerializer

tags = ["Profiles"]


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwner]

    @extend_schema(
        summary="Retrieve Profile",
        description="""
            This endpoint allows a user to retrieve his/her profile.
        """,
        tags=tags,
    )
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Update Profile",
        description="""
                This endpoint allows a user to update his/her profile.
            """,
        tags=tags,
        request={"multipart/form-data": serializer_class},
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Deactivate account",
        description="""
            This endpoint allows a user to deactivate his/her account.
        """,
        tags=tags,
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={"message": "User Account Deactivated"})


class ShippingAddressesView(APIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsOwner]

    @extend_schema(
        summary="Shipping Addresses Fetch",
        description="""
            This endpoint returns all shipping addresses associated with a user.
        """,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        shipping_addresses = ShippingAddress.objects.filter(user=user)
        serializer = self.serializer_class(shipping_addresses, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Create Shipping Address",
        description="""
            This endpoint allows a user to create a shipping address.
        """,
        tags=tags,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address, _ = ShippingAddress.objects.get_or_create(user=user, **data)
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data, status=201)


class ShippingAddressViewID(APIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsOwner]

    def get_object(self, user, shipping_id):
        shipping_address = ShippingAddress.objects.get_or_none(id=shipping_id)
        if shipping_address is not None:
            self.check_object_permissions(self.request, shipping_address)
        return shipping_address

    @extend_schema(
        summary="Shipping Address Fetch ID",
        description="""
            This endpoint returns a single shipping address associated with a user.
        """,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Update Shipping Address ID",
        description="""
            This endpoint allows a user to update his/her shipping address.
        """,
        tags=tags,
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address = set_dict_attr(shipping_address, data)
        shipping_address.save()
        serializer = self.serializer_class(shipping_address)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Delete Shipping Address ID",
        description="""
            This endpoint allows a user to delete his/her shipping address.
        """,
        tags=tags,
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs["id"])
        if not shipping_address:
            return Response(data={"message": "Shipping Address does not exist!"}, status=404)
        shipping_address.delete()
        return Response(data={"message": "Shipping address deleted successfully"}, status=200)


class OrdersView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]

    @extend_schema(
        operation_id="orders_view",
        summary="Orders Fetch",
        description="""
            This endpoint returns all orders for a particular user.
        """,
        tags=tags
    )
    def get(self, request):
        user = request.user
        orders = (Order.objects.filter(user=user).select_related("user")
                  .prefetch_related("orderitems", "orderitems__product")
                  .order_by("-created_at"))
        serializer = self.serializer_class(orders, many=True)
        return Response(data=serializer.data, status=200)


class OrderItemView(APIView):
    serializer_class = CheckItemOrderSerializer
    permission_classes = [IsOwner, ]

    @extend_schema(
        operation_id="orders_items_view",
        summary="Item Orders Fetch",
        description="""
            This endpoint returns all items orders for a particular user.
        """,
        tags=tags,

    )
    def get(self, request, **kwargs):
        order = Order.objects.get_or_none(tx_ref=kwargs["tx_ref"])
        if not order or order.user != request.user:
            return Response(data={"message": "Order does not exist!"}, status=404)
        order_items = OrderItem.objects.filter(order=order)
        serializer = self.serializer_class(order_items, many=True)
        return Response(data=serializer.data, status=200)