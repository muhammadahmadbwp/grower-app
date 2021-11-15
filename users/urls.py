from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views
from rest_framework_simplejwt import views as jwt_views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'api/user', views.UserView, basename='user-api')
router.register(r'api/activate_user', views.ActivateUserView, basename='activate-user-api')
router.register(r'api/send_otp', views.SendOtpView, basename='send-otp-api')
router.register(r'api/validate_user', views.ValidateUserView, basename='validate-user-api')
router.register(r'api/dump_growers_csv', views.DumpGrowerDataView, basename='dump-grower-api')

urlpatterns = [
    path('', include(router.urls)),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/reset_password/', views.ResetPasswordView.as_view(), name='reset-password-api'),
    path('api/change_password/', views.ChangePasswordView.as_view(), name='reset-password-api')
]