from rest_framework import serializers
from documents.models import SampleDocuments
from user.serializers import UserSerializer


class SampleDocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SampleDocuments
        fields = ["cv","sop","bank_statement", "loan_letter", "recommendation", "work_experience", "affidavit","cover_letter", "marriage_evidence","relationship","workflow"]
        read_only_fields = ['created_at','updated_at','created_by','updated_by']


class SampleDocumentViewSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()
    class Meta(SampleDocumentSerializer.Meta):
        model = SampleDocuments
        fields = SampleDocumentSerializer.Meta.fields+['id','created_at','updated_at','created_by','updated_by']