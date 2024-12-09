from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import CreateUserSerializer


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            if user.is_staff:
                refresh.payload.update({'group': 'admin'})
            else:
                refresh.payload.update({'group': 'user', 'role': user.account_type})

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


