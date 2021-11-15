from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat import views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()

router.register(r'message', views.MessageView, basename='message-api')

urlpatterns = [
    path('api/', include(router.urls)),
]