from django.db.models import fields
from users.models import CustomUser
from rest_framework import serializers
from growerfields.models import GrowerFieldModel, FieldCoordsByGrowerModel, FieldCoordsBySurveyorModel, CropVarietyType, CropVarietySubType


class CropVarietyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CropVarietyType
        fields = "__all__"


class CropVarietySubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CropVarietySubType
        fields = "__all__"


class CropVarietyTypeSubTypeSerializer(serializers.ModelSerializer):
    crop_variety_sub_type = CropVarietySubTypeSerializer(many=True)

    class Meta:
        model = CropVarietyType
        fields = ['id', 'crop_variety', 'crop_variety_sub_type']


class FieldCoordsByGrowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldCoordsByGrowerModel
        fields = "__all__"


class FieldCoordsBySurveyorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldCoordsBySurveyorModel
        fields = "__all__"


class GrowerFieldSerailizer(serializers.ModelSerializer):
    
    grower_coords = FieldCoordsByGrowerSerializer(many=True)
    surveyor_coords = FieldCoordsBySurveyorSerializer (many=True)

    class Meta:
        model = GrowerFieldModel
        fields = ['id', 'grower', 'crop_variety', 'crop_variety_sub_type', 'field_name', 'land_type', 'area_unit', 'area_auto', 'area_manual', 'plantation_date', 'plantation_type', 'multi_fields', 
        'country', 'province', 'city', 'village', 'field_status', 'created_at', 'updated_at', 'surveyor', 'surveyed_at', 'grower_coords', 'surveyor_coords']

    def create(self, validated_data):
        grower_field_coords_data = validated_data.pop('grower_coords')
        surveyor_field_coords_data = validated_data.pop('surveyor_coords')
        grower_field_coords_serializer = self.fields['grower_coords']
        instance = self.Meta.model(**validated_data)
        instance.save()
        if grower_field_coords_data:
            grower_field_coords = grower_field_coords_serializer.create(grower_field_coords_data)
            instance.grower_coords.set(grower_field_coords)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.field_status = validated_data.pop('field_status', instance.field_status)
        instance.surveyor = validated_data.pop('surveyor', instance.surveyor)
        instance.surveyed_at = validated_data.pop('surveyed_at', instance.surveyed_at)
        surveyor_field_coords_data = validated_data.pop('surveyor_coords')
        surveyor_field_coords_serializer = self.fields['surveyor_coords']
        instance.save()
        if surveyor_field_coords_data:
            surveyor_field_coords = surveyor_field_coords_serializer.create(surveyor_field_coords_data)
            instance.surveyor_coords.set(surveyor_field_coords)
        instance.save()
        return instance


class GetGrowerFieldSerailizer(serializers.ModelSerializer):

    grower_coords = FieldCoordsByGrowerSerializer(many=True)
    surveyor_coords = FieldCoordsBySurveyorSerializer (many=True)

    class Meta:
        model = GrowerFieldModel
        fields = ['id', 'grower', 'crop_variety', 'crop_variety_sub_type', 'field_name', 'land_type', 'area_unit', 'area_auto', 'area_manual', 'plantation_date', 'plantation_type', 'multi_fields', 
        'country', 'province', 'city', 'village', 'field_status', 'created_at', 'updated_at', 'surveyor', 'surveyed_at', 'grower_coords', 'surveyor_coords']
        depth = 1


class GetGrowerSurveyorFieldSerailizer(serializers.ModelSerializer):

    grower_coords = FieldCoordsByGrowerSerializer(many=True)
    surveyor_coords = FieldCoordsBySurveyorSerializer (many=True)

    class Meta:
        model = GrowerFieldModel
        fields = ['id', 'grower', 'crop_variety', 'field_name', 'land_type', 'area_unit', 'area_auto', 'area_manual', 'plantation_date', 'plantation_type', 'multi_fields', 
        'country', 'province', 'city', 'village', 'field_status', 'created_at', 'updated_at', 'surveyor', 'surveyed_at', 'grower_coords', 'surveyor_coords']


class GrowerRelatedToGrowerFieldSerializer(serializers.ModelSerializer):

    grower_id = GetGrowerSurveyorFieldSerailizer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'email', 'user_type', 'grower_id']


class SurveyorRelatedToGrowerFieldSerializer(serializers.ModelSerializer):

    surveyor_id = GetGrowerSurveyorFieldSerailizer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'father_name', 'mobile_number', 'cnic', 'email', 'user_type', 'surveyor_id']