from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response("test", status=status.HTTP_200_OK)
