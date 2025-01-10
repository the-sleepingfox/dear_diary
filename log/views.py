from django.shortcuts import render
from .models import Entry
from .serializers import EntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class GetEveryThing(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        entries= Entry.objects.all()
        serializer= EntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterUser(APIView):
    permission_classes= [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Please enter username and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exist, please use another username"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "User created successfully",
                "refresh": str(refresh),
                "token": str(refresh.access_token)
            },
            status=status.HTTP_201_CREATED
        )

class GetRoutes(APIView):
    def get(self, request):
        routes=[
            {'GET': 'api/'},
            {'GET': 'api/entry/'},
            {'GET': 'api/entry/id/'},
            {'POST': 'api/entry/new'},
            # {'PUT': 'api/entry/<str:pk>/'},
            {'DELETE': 'api/entry/id/'},
        ]
        return Response(routes)

class NewEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EntryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            entries = Entry.objects.get(owner= request.user)
            serializer = EntrySerializer(entries, many=True)
            return Response(serializer.data)
        except Entry.DoesNotExist:
            return Response({'error': 'No entries found'}, status=status.HTTP_404_NOT_FOUND)


class SingleEntry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            entry = Entry.objects.get(pk= pk)
            serializer= EntrySerializer(entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        owner= request.user
        try:
            entry = Entry.objects.get(pk= pk)
            serializer= EntrySerializer(entry, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            entry = Entry.objects.get(pk= pk)
            entry.delete()
            return Response({'message': f'Entry with {entry.heading} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status=status.HTTP_404_NOT_FOUND)
