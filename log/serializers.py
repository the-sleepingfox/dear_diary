from rest_framework import serializers
from .models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model= Entry
        fields= ['id', 'owner', 'created_at', 'updated_at', 'heading', 'content']