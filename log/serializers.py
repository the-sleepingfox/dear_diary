from rest_framework import serializers
from .models import Entry
from django.contrib.auth.models import User

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['owner']