  
from django.urls import path,include
from user import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()

router.register('user', views.UserCreateApi, basename='user')
# router.register('student/authenticate/list/', views.StudentListApi, basename='student-list')

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/logout/blacklist/', views.BlacklistTokenUpdateView.as_view(),name='blacklist'),
    path('api/logout/', views.LogoutAPIView.as_view(),name="logout"),
    path('api/token/', views.ObtainTokenPairWithUsernameView.as_view(), name='login'),
    path('api/user/details/', views.UserDetails.as_view(), name='userdetails'),
    path('api/user/changepassword/', views.ChangePassword.as_view(), name='passwordchange'),
    path('api/create/student/login/',views.StudentLoginCreateAPI.as_view(),name='studentlogin'),

    path('api/student/authenticate/list/',views.StudentListApi.as_view(),name="student-list"),
    path('api/staff/list/',views.StaffListApi.as_view(),name="staff-list"),

    path('api/',include(router.urls)),
]
