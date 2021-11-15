from django.db import models
from django.db.models.fields import IntegerField
from users.models import CustomUser

# Create your models here.


class CropVarietyType(models.Model):

    crop_variety = models.CharField(max_length=50)


class CropVarietySubType(models.Model):

    crop_variety_type = models.ForeignKey(CropVarietyType, on_delete=models.CASCADE, related_name='crop_variety_sub_type')
    crop_variety_sub_type = models.CharField(max_length=50)


class GrowerFieldModel(models.Model):

    OWNED = 1
    LEASED = 2

    LAND_TYPE_CHOICES = (
        (OWNED, 'owned'),
        (LEASED, 'leased')
    )

    RATOON = 1
    PLANTED = 2

    PLANTATION_TYPE_CHOICES = (
        (RATOON, 'ratoon'),
        (PLANTED, 'planted')
    )

    ACTIVE = 1
    DELETION_REQUESTED = 2
    DELETED = 3

    FIELD_STATUS_CHOICES = (
        (ACTIVE, 'active'),
        (DELETION_REQUESTED, 'deletion_requested'),
        (DELETED, 'deleted')
    )

    grower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grower_id')
    crop_variety = models.ForeignKey(CropVarietyType, on_delete=models.CASCADE, related_name='crop_variety_type')
    crop_variety_sub_type = models.ForeignKey(CropVarietySubType, on_delete=models.CASCADE, blank=True, null=True, related_name='crop_variety_subtype')
    field_name = models.CharField(max_length=100)
    land_type = models.PositiveSmallIntegerField(choices=LAND_TYPE_CHOICES)
    area_unit = models.CharField(max_length=50)
    area_auto = models.FloatField()
    area_manual = models.FloatField()
    plantation_date = models.DateField()
    plantation_type = models.PositiveSmallIntegerField(choices=PLANTATION_TYPE_CHOICES)
    multi_fields = models.BooleanField(blank=True, null=True)
    country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    field_status = models.PositiveSmallIntegerField(choices=PLANTATION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    surveyor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='surveyor_id')
    surveyed_at = models.DateTimeField(blank=True, null=True)


class FieldCoordsByGrowerModel(models.Model):

    field = models.ForeignKey(GrowerFieldModel, on_delete=models.CASCADE, null=True, related_name='grower_coords')
    latitude = models.FloatField()
    longitude = models.FloatField()
    coords_seq = IntegerField()


class FieldCoordsBySurveyorModel(models.Model):

    field = models.ForeignKey(GrowerFieldModel, on_delete=models.CASCADE, null=True, related_name='surveyor_coords')
    latitude = models.FloatField()
    longitude = models.FloatField()
    coords_seq = IntegerField()