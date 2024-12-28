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
            {'GET': 'api/entries/'},
        ]
        return Response(routes)

class EntryList(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        entries= Entry.objects.all()
        serializer= EntrySerializer(entries, many= True)
        return Response(serializer.data)
    
class SingleEntry(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request, pk):
        try:
            entry= Entry.objects.get(pk= pk)
            serializer= EntrySerializer(entry)
            return Response(serializer.data, status= 200)
        except Entry.DoesNotExist:
            return Response({'error': 'Entry does not exist'}, status= 404)
        
    def put(self, request, pk):
        pass