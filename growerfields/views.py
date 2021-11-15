from users.models import CustomUser
from growerfields.models import GrowerFieldModel, CropVarietyType, CropVarietySubType
from rest_framework.response import Response
from rest_framework import viewsets, status
from growerfields.serializers import (
    GrowerFieldSerailizer, GetGrowerFieldSerailizer, GrowerRelatedToGrowerFieldSerializer, SurveyorRelatedToGrowerFieldSerializer, CropVarietyTypeSerializer,
    CropVarietySubTypeSerializer, CropVarietyTypeSubTypeSerializer
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from django.db.models import Q


class custom_serializer_errors:

    def serializer_errors(self, msg):
        error_message = ""
        for key, value in msg.items():
            msg = f"{key}: {value[0]} "
            error_message += str(msg)
        return error_message


class GrowerFieldView(viewsets.ViewSet):

    # permission_classes = [IsAuthenticated]

    def get_queryset(self, request):

        queryset = GrowerFieldModel.objects.all()
        surveyor_id = self.request.query_params.get('surveyor_id', None)
        grower_id = self.request.query_params.get('grower_id', None)
        grower_fields_by_surveyor_id = self.request.query_params.get('grower_fields_by_surveyor_id', None)
        growers_distinct = self.request.query_params.get('growers_distinct', None)
        if surveyor_id is not None:
            queryset = queryset.filter(surveyor=surveyor_id)
        if grower_id is not None:
            queryset = queryset.filter(grower=grower_id)
        if grower_fields_by_surveyor_id is not None and grower_fields_by_surveyor_id == 'assigned_fields':
            queryset = queryset.filter(Q(surveyor=surveyor_id), Q(grower=grower_id))
        if growers_distinct is not None and growers_distinct == 'distinct':
            queryset = queryset.filter(surveyor=surveyor_id).distinct('grower')
        return queryset

    def create(self, request):
        request_data = request.data
        serializer = GrowerFieldSerailizer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "success":True, "message":"grower field added successfully"}, status=status.HTTP_200_OK)
        serializer_errors = custom_serializer_errors()
        serializer_errors = serializer_errors.serializer_errors(serializer.errors)
        return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = GrowerFieldModel.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = GrowerFieldSerailizer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "success":True, "message":"field data updated successfully"}, status=status.HTTP_200_OK)
        serializer_errors = custom_serializer_errors()
        serializer_errors = serializer_errors.serializer_errors(serializer.errors)
        return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        queryset = GrowerFieldModel.objects.all()
        id_list = request.data['ids']
        data = []
        for id in id_list:
            item = get_object_or_404(queryset, pk=id)
            serializer = GrowerFieldSerailizer(instance=item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                serializer_errors = custom_serializer_errors()
                serializer_errors = serializer_errors.serializer_errors(serializer.errors)
                return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)
            data.append(serializer.data)
        return Response({"data":data, "success":True, "message":"fields assigned to the surveyor successfully"}, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = GetGrowerFieldSerailizer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = GrowerFieldModel.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = GetGrowerFieldSerailizer(item)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        queryset = GrowerFieldModel.objects.all().filter(pk=pk).delete()
        return Response({"data":{}, "success":True, "message":"grower field deleted successfully"}, status=status.HTTP_200_OK)


class GrowerRelatedToGrowerFieldView(viewsets.ViewSet):

    def list(self, request):
        queryset = CustomUser.objects.all().filter(user_type=3)
        serializer = GrowerRelatedToGrowerFieldSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.all().filter(pk=pk, user_type=3)
        serializer = GrowerRelatedToGrowerFieldSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)


class SurveyorRelatedToGrowerFieldView(viewsets.ViewSet):

    def list(self, request):
        queryset = CustomUser.objects.all().filter(user_type=2)
        serializer = SurveyorRelatedToGrowerFieldSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.all().filter(pk=pk, user_type=2)
        serializer = SurveyorRelatedToGrowerFieldSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)


class CropVarietyTypeView(viewsets.ViewSet):

    def get_queryset(self, request):

        queryset = CropVarietyType.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = CropVarietyTypeSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)


class CropVarietySubTypeView(viewsets.ViewSet):

    def get_queryset(self, request):

        queryset = CropVarietyType.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = CropVarietySubTypeSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)


class CropVarietyTypeSubTypeView(viewsets.ViewSet):

    def get_queryset(self, request):
        queryset = CropVarietyType.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = CropVarietyTypeSubTypeSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)