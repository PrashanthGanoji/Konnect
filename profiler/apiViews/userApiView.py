
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiler.serializers.user_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class UserList(APIView):
    """
    Creates the user.
    """
    def get(self, request, format='json'):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id, format='json'):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)