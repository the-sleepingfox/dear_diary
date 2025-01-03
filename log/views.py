from django.shortcuts import render
from .models import Entry
from .serializers import EntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


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
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
class EntryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
    
class SingleEntry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            entry = Entry.objects.get(pk= pk)
            serializer= EntrySerializer(entry)
            return Response(serializer.data, status=200)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status=404)
        

    def delete(self, request, pk):
        try:
            entry = Entry.objects.get(pk= pk)
            entry.delete()
            return Response({'message': f'Entry with {entry.heading} deleted successfully'}, status=204)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status=404)
