from rest_framework import serializers, viewsets
from .models import CsvUpload

class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvUpload
        fields = '__all__'

class CsvViewSet(viewsets)