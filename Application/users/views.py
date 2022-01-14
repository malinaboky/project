from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import *
from rest_framework.response import Response

from .renderers import UserJSONRenderer
from .serializers import *


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserTokenSerializer

    def retrieve(self, request, *args, **kwargs):
        print(request.user)
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
