from users.models import CustomUser
from users.serializers import (
    GetCustomUserSerializer, AdminUserSerializer, SurveyorUserSerializer, GrowerUserSerializer, ResetPasswordSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
import datetime
from django.utils import timezone
from random import randint
import os
from twilio.rest import Client


# Create your views here.


class custom_serializer_errors:
    
    def serializer_errors(self, msg):
        error_message = ""
        for key, value in msg.items():
            msg = f"{key}: {value[0]} "
            error_message += str(msg)
        return error_message


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # token_obtain_pair = TokenObtainPairView.as_view()


class UserView(viewsets.ViewSet):

    def get_queryset(self, request):

        queryset = CustomUser.objects.all()
        user_type = self.request.query_params.get('user_type', None)
        if user_type is not None:
            queryset = queryset.filter(user_type=user_type)
        return queryset

    def create(self, request):
        request_data = request.data
        if request_data['user_type'] == 1 and (request_data['notification_token'] != '' and request_data['notification_token'] is not None):
            serializer = AdminUserSerializer(data=request_data)
        elif request_data['user_type'] == 2 and (request_data['notification_token'] != '' and request_data['notification_token'] is not None):
            if 'password' not in request_data:
                request_data['password'] = 'Surveyor@TSI'
            serializer = SurveyorUserSerializer(data=request_data)
        elif request_data['user_type'] == 3 and (request_data['notification_token'] != '' and request_data['notification_token'] is not None):
            if 'password' not in request_data:
                request_data['password'] = 'Grower@TSI'
            serializer = GrowerUserSerializer(data=request_data)
        else:
            return Response({"data":{}, "success":False, "message":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
        else:
            serializer_errors = custom_serializer_errors()
            serializer_errors = serializer_errors.serializer_errors(serializer.errors)
            return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":serializer.data, "success":True, "message":"user created successfully"}, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = GetCustomUserSerializer(queryset, many=True)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = CustomUser.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = GetCustomUserSerializer(item)
        return Response({"data":serializer.data, "success":True, "message":"data found"}, status=status.HTTP_200_OK)

    def delete(self, request):
        mobile_number = self.request.query_params.get('mobile_number', None)
        mobile_number = '+' + mobile_number.strip()
        queryset = CustomUser.objects.all()
        if mobile_number is not None:
            queryset.filter(mobile_number=mobile_number).delete()
        return Response({"data":{}, "success":True, "message":"user record deleted successfully"}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        queryset = CustomUser.objects.all().filter(pk=pk).delete()
        return Response({"data":{}, "success":True, "message":"user record deleted successfully"}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):

        queryset = CustomUser.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        notification_token = self.request.query_params.get('notification_token', None)
        log_out = self.request.query_params.get('log_out', None)
        if notification_token == 'yes':
            item.notification_token = request.data['notification_token']
            request.data['notification_token']
            item.save()
            return Response({"data":{}, "success":True, "message":"notification_token updated successfully"}, status=status.HTTP_200_OK)
        elif log_out == 'yes':
            item.notification_token = None
            item.save()
            return Response({"data":{}, "success":True, "message":"user logged out successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"data":{}, "success":False, "message":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(viewsets.ViewSet):

    def create(self, request):
        request_data = request.data
        try:
            user = CustomUser.objects.get(mobile_number=request_data['mobile_number'])
        except:
            return Response({"data":{}, "success":False, "message":"no user with the given mobile number found in the system"}, status=status.HTTP_400_BAD_REQUEST)
        current_time = datetime.datetime.utcnow().replace(tzinfo=None)
        database_time = user.updated_at.replace(tzinfo=None)
        time_difference = ((current_time-database_time).total_seconds())/60
        if (time_difference < 30):
            if user.activation_otp == request_data['activation_otp'] and user.user_type == 3 and user.is_active == False:
                user.is_active = True
                user.save()
        else:
            return Response({"data":{}, "success":False, "message":"otp has expired. please generate new otp"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetCustomUserSerializer(user)
        return Response({"data":serializer.data, "success":True, "message":"user activated successfully"}, status=status.HTTP_200_OK)


def generate_otp(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class SendOtpView(viewsets.ViewSet):

    def create(self, request):
        request_data = request.data
        try:
            user = CustomUser.objects.get(mobile_number=request_data['mobile_number'])
        except:
            user = None
        otp = generate_otp(4)
        if user:
            user.updated_at = timezone.now()
            user.activation_otp = otp
            user.save()
            user_exist = True
        else:
            user_exist = False
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        try:
            message = client.messages.create(
                                        body=f"TSI Grower App account verification code: {otp}",
                                        from_=os.environ['TWILIO_PHONE_NUMBER'],
                                        # media_url=['https://demo.twilio.com/owl.png'],
                                        to=request_data['mobile_number']
                                    )
            print(message.sid)
            return Response({"data":{"activateion_otp":otp, "user_exist":user_exist}, "success":True, "message":"otp sent successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"data":{}, "success":False, "message":f"{otp} otp not sent to {request_data['mobile_number']}"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    def put(self, request, *args, **kwargs):
        request_data = request.data
        try:
            user = CustomUser.objects.get(mobile_number=request_data['mobile_number'])
        except:
            return Response({"data":{}, "success":False, "message":"no user with the given mobile number found in the system"}, status=status.HTTP_400_BAD_REQUEST)
        request_data['updated_at'] = timezone.now()
        
        current_time = datetime.datetime.utcnow().replace(tzinfo=None)
        database_time = user.updated_at.replace(tzinfo=None)
        time_difference = ((current_time-database_time).total_seconds())/60
        if (time_difference < 30):
            if user.activation_otp == request_data['activation_otp']:
                serializer = ResetPasswordSerializer(instance=user, data=request_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":{}, "success":True, "message":"password updated successfully"}, status=status.HTTP_200_OK)
                serializer_errors = custom_serializer_errors()
                serializer_errors = serializer_errors.serializer_errors(serializer.errors)
                return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":{}, "success":False, "message":"otp has expired. please generate new otp"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        request_data = request.data
        try:
            user = CustomUser.objects.get(pk=request.user.id)
        except:
            return Response({"data":{}, "success":False, "message":"no user with the given mobile number found in the system"}, status=status.HTTP_400_BAD_REQUEST)
        request_data['updated_at'] = timezone.now()
        serializer = ResetPasswordSerializer(instance=user, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":{}, "success":True, "message":"password updated successfully"}, status=status.HTTP_200_OK)
        serializer_errors = custom_serializer_errors()
        serializer_errors = serializer_errors.serializer_errors(serializer.errors)
        return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_400_BAD_REQUEST)


class ValidateUserView(viewsets.ViewSet):

    def list(self, request):
        mobile_number = self.request.query_params.get('mobile_number', None)
        mobile_number = '+' + mobile_number.strip()
        try:
            CustomUser.objects.get(mobile_number=mobile_number)
            user_exist = True
            return Response({"data":{"user_exist":user_exist}, "success":True, "message":"user found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            user_exist = False
            return Response({"data":{"user_exist":user_exist}, "success":False, "message":"no user with the given mobile number found in the system"}, status=status.HTTP_200_OK)


class DumpGrowerDataView(viewsets.ViewSet):

    def create(self, request):
        try:
            csv_file = request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")	
            lines = file_data.split("\n")
            data = list()
            for line in lines[1:-1]:
                print(len(lines))					
                fields = line.split(",")
                data_dict = dict()
                data_dict["user_name"] = fields[0]
                data_dict["father_name"] = fields[1]
                data_dict["cnic"] = fields[2]
                data_dict["mobile_number"] = fields[3]
                data_dict["password"] = 'admin12345'
                data_dict["user_type"] = 3
                data_dict["notification_token"] = {}
                data_dict["grower_detail"] = [{}]
                serializer = GrowerUserSerializer(data=data_dict)
                if serializer.is_valid():
                    serializer.save()
                else:
                    serializer_errors = custom_serializer_errors()
                    serializer_errors = serializer_errors.serializer_errors(serializer.errors)
                    return Response({"data":{}, "success":False, "message":serializer_errors}, status=status.HTTP_200_OK)
                data.append(serializer.data)
        except:
            pass
            # return Response({"data":{}, "success":False, "message":"unexpected error occured"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":data, "success":True, "message":"csv dumped successfully"}, status=status.HTTP_200_OK)