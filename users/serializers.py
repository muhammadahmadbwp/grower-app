from django.utils import timezone
from rest_framework import serializers
from users.models import CustomUser, AdminDetails, SurveyorDetails, GrowerDetails
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
import os


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            user = CustomUser.objects.get(mobile_number=attrs["mobile_number"])
        except ObjectDoesNotExist:
            result = dict()
            result['data'] = {}
            result['success'] = False
            result['message'] = 'no active user with the given mobile number exist in the system'
            return result
        if user.is_active:
            data = super().validate(attrs)
            data.update({'id': self.user.id})
            data.update({'last_login': self.user.last_login})
            data.update({'user_name': self.user.user_name})
            data.update({'user_type': self.user.user_type})
            data.update({'notification_token': self.user.notification_token})
            data.update({'is_active': self.user.is_active})
            data.update({'is_staff': self.user.is_staff})
            data.update({'is_superuser': self.user.is_superuser})
            result = dict()
            result['data'] = dict(data)
            result['success'] = True
            result['message'] = 'user logged in successfully'
            user.last_login = timezone.now()
            user.save()
        else:
            result = dict()
            result['data'] = dict()
            result['data']['last_login'] = user.last_login
            result['data']['is_active'] = user.user_name
            result['data']['user_type'] = user.user_type
            result['data']['notification_token'] = user.notification_token
            result['data']['is_active'] = user.is_active
            result['data']['is_staff'] = user.is_staff
            result['data']['is_superuser'] = user.is_superuser
            result['success'] = False
            result['message'] = 'user login not successful'
        return result


class AdminDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDetails
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    admin_detail = AdminDetailsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'password', 'email', 'user_type', 'notification_token', 'is_staff', 'is_active', 'admin_detail')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.get('user_type', None)
        admin_detail_data = validated_data.pop('admin_detail')
        admin_detail_serializer = self.fields['admin_detail']
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        if user_type is not None:
            instance.is_staff = True
            instance.is_active = True
        if admin_detail_data:
            admin_detail = admin_detail_serializer.create(admin_detail_data)
            instance.admin_detail.set(admin_detail)
        instance.save()
        return instance


class SurveyorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyorDetails
        fields = "__all__"


class SurveyorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    surveyor_detail = SurveyorDetailsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'password', 'email', 'user_type', 'notification_token', 'is_staff', 'is_active', 'surveyor_detail')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.get('user_type', None)
        surveyor_detail_data = validated_data.pop('surveyor_detail')
        surveyor_detail_serializer = self.fields['surveyor_detail']
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        if user_type is not None:
            instance.is_staff = True
            instance.is_active = True
        if surveyor_detail_data:
            surveyor_detail = surveyor_detail_serializer.create(surveyor_detail_data)
            instance.surveyor_detail.set(surveyor_detail)
        instance.save()
        return instance


class GrowerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowerDetails
        fields = "__all__"


class GrowerUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    grower_detail = GrowerDetailsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'password', 'email', 'user_type', 'notification_token', 'is_staff', 'is_active', 'grower_detail')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.get('user_type', None)
        grower_detail_data = validated_data.pop('grower_detail')
        grower_detail_serializer = self.fields['grower_detail']
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        if user_type is not None:
            instance.is_staff = False
            instance.is_active = True
        if grower_detail_data:
            grower_detail = grower_detail_serializer.create(grower_detail_data)
            instance.grower_detail.set(grower_detail)
        instance.save()
        return instance


class GetCustomUserSerializer(serializers.ModelSerializer):
    admin_detail = AdminDetailsSerializer(many=True, read_only=True)
    surveyor_detail = SurveyorDetailsSerializer(many=True, read_only=True)
    grower_detail = GrowerDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'email', 'user_type', 'notification_token', 'is_staff', 'is_active', 'admin_detail', 'surveyor_detail', 'grower_detail']
        depth = 1


class  ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['password', 'updated_at']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', instance.password)
        instance.updated_at = validated_data.pop('updated_at', instance.updated_at)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance