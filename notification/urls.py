from django.urls import path,include
from notification import views


urlpatterns = [
    path('api/notification/', views.NotificationApi.as_view(), name='notification'),
]