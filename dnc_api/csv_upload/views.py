from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .serializer import CsvUploadSerializer, CsvViewSet
from rest_framework import serializers, viewsets, status
from .models import CsvUpload

# importing required libraries for CSV FILE
import csv
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from rest_framework.decorators import action

class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvUpload
        fields = '__all__'

# file location
fs = FileSystemStorage(location="tmp")

class CsvViewSet(viewsets.ModelViewSet):

    queryset = CsvUpload.objects.all()
    serializer_class = CsvUploadSerializer

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        if "file" not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES["file"]
        # to read the content of the file
        content = file.read()
        # to create a file object
        file_content = ContentFile(content)

        # file name
        file_name = fs.save("_tmp.csv", file_content)

        # file path
        tmp_file_path = fs.path(file_name)

        # opening the file
        csv_file = open(tmp_file_path, errors='ignore')

        # reading the file
        csv_reader = csv.reader(csv_file)

        # skip headers of the file
        next(csv_reader)

        # creating a list to store the data
        data_list = []

        for id_, row in enumerate(csv_reader):
            (
                name,
                url,
            ) = row

            # append the data to the list
            data_list.append(
                CsvUpload(name=name, url=url)
            )

        # saving the data to the database
        CsvUpload.objects.bulk_create(data_list)

        return Response({"status": "success"}, status=status.HTTP_200_OK)
