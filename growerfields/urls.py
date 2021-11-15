from django.urls import path, include
from rest_framework.routers import DefaultRouter
from growerfields import views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'api/grower_field', views.GrowerFieldView, basename='grower-field-api')
router.register(r'api/grower_user_field', views.GrowerRelatedToGrowerFieldView, basename='grower-user-field-api')
router.register(r'api/crop_variety_type', views.CropVarietyTypeView, basename='crop-variety-type-api')
router.register(r'api/crop_variety_sub_type', views.CropVarietySubTypeView, basename='crop-variety-sub-type-api')
router.register(r'api/crop_variety_type_sub_type', views.CropVarietyTypeSubTypeView, basename='crop-variety-type-sub-type-api')

urlpatterns = [
    path('', include(router.urls)),
]