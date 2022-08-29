from django.shortcuts import render
from documents.models import SampleDocuments
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



from documents.serializers import SampleDocumentSerializer, SampleDocumentViewSerializer



# Create your views here.

class SampleDocumentAPI(viewsets.ModelViewSet):
    queryset = SampleDocuments.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SampleDocumentSerializer


    def get_serializer_class(self):
        if self.action == 'create':
            return SampleDocumentSerializer
        elif self.action == 'update':    
            return SampleDocumentSerializer    
        elif self.action == 'partial_update':    
            return SampleDocumentSerializer
        else:
            return SampleDocumentViewSerializer  

    def create(self, request, **kwargs):
        if self.request.user.is_active:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        return Response({"Error": "User is not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
             

    def update(self, request, **kwargs):
        if self.request.user.is_active:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        return Response({"Error": "User is not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    