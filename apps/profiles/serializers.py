from rest_framework import serializers




class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(required=False)
    account_type = serializers.CharField(read_only=True)


class ShippingAddressSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    address = serializers.CharField(max_length=1000)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField()
    zipcode = serializers.IntegerField()





