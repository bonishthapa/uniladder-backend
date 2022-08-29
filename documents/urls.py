from django.urls import path,include
from rest_framework.routers import DefaultRouter
from documents import views

router = DefaultRouter()

router.register('sample/documents', views.SampleDocumentAPI, basename='sample-document')

urlpatterns = [
    path('api/',include(router.urls)),
    
]