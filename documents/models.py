from django.db import models

from user.models import User

# Create your models here.
class SampleDocuments(models.Model):
    cv = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    sop = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    bank_statement = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    loan_letter = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    recommendation = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    work_experience = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    affidavit = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    cover_letter = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    marriage_evidence = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    relationship = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    workflow = models.FileField(upload_to = 'sample_documents', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sample_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sample_updated_by',blank=True,null=True)