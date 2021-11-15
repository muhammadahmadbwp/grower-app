from chat.models import MessageModel
from chat.serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from django.shortcuts import render


class custom_serializer_errors:
    
    def serializer_errors(self, msg):
        error_message = ""
        for key, value in msg.items():
            msg = f"{key}: {value[0]} "
            error_message += str(msg)
        return error_message


class MessageView(viewsets.ViewSet):

    def create(self, request):
        request_data = request.data
        serializer = MessageSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "success":True, "message":"message sent"}, status=status.HTTP_200_OK)
        serializer_errors = custom_serializer_errors()
        serializer_errors = serializer_errors.serializer_errors(serializer.errors)
        return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = MessageModel.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(instance=item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "success":True, "message":"message updated"}, status=status.HTTP_200_OK)
        serializer_errors = custom_serializer_errors()
        serializer_errors = serializer_errors.serializer_errors(serializer.errors)
        return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })