import os
from django.db import models
from django.dispatch import receiver
# from notification.models import Notification
from user.models import User



class University(models.Model):
    name=models.CharField(max_length=250)
    location=models.CharField(max_length=250,blank=True)
    link=models.CharField(max_length=250,blank=True)
    logo=models.FileField(upload_to="university",blank=True)
    scholarship_detail=models.TextField(blank=True)
    min_deposit_detail=models.TextField(blank=True)
    remark=models.TextField(blank=True)
    entry_requirement=models.TextField(blank=True)
    credibility_qa=models.FileField(upload_to="university",blank=True)
    work_flow=models.FileField(upload_to="university",blank=True)
    bank_detail=models.FileField(upload_to="university",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='university_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='university_updated_by',blank=True,null=True)

    def __str__(self):
        return self.name

class StudentIntake(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name        

# Create your models here.
class StudentDetail(models.Model):

    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
    ]
    LEVEL_CHOICES=[
        ('Undergraduate','Undergraduate'),
        ('Postgraduate','Postgraduate'),
        ('Phd','Phd'),
    ]
    STATUS_CHOICES=[
        ('File Not Submitted', 'File Not Submitted'),
        ('File Submitted','File Submitted'),
        ('Conditional Offer','Conditional Offer'),
        ('Unconditional Offer','Unconditional Offer'),
        ('Offer rejected','Offer rejected'),
        ('Deposit Paid','Deposit Paid'),
        ('Interview','Interview'),
        ('CAS Requested','CAS Requested'),
        ('CAS Issued','CAS Issued'),
        ('VFS Appointment','VFS Appointment'),
        ('Visa Granted','Visa Granted'),
        ('Visa Rejected','Visa Rejected'),
        ('Inquiry','Inquiry'),
        ('On Hold','On Hold'),
        ('Deferred','Deferred'),
        ('Enrolled','Enrolled'),
    ]
    DEPENDENT_CHOICES=[
        ('Yes','Yes'),
        ('No','No'),
    ]

    EMAIL_ACCESS=[
        ('Yes','Yes'),
        ('No','No'),
    ]

    FINACIAL_STATUS=[
        ('Loan','Loan'),
        ('Cash','Cash'),
    ]

    name = models.CharField(max_length=100, blank=False)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    actual_email = models.EmailField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, blank=True, null=True)
    academic = models.CharField(max_length=200, blank=True, null=True)
    percentage = models.CharField(max_length=10, blank=True, null=True)
    english = models.CharField(max_length=30, blank=True, null=True) 
    intake = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES,blank=True, null=True)
    dependent = models.CharField(max_length=50, choices=DEPENDENT_CHOICES,blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    university = models.CharField(max_length=200, blank=True, null=True)
    course = models.CharField(max_length=200, blank=True, null=True)
    amount_paid = models.CharField(max_length=20, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    recommendation = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)

    email_access = models.CharField(max_length=10, choices=EMAIL_ACCESS, blank=True, null=True)
    financial_status = models.CharField(max_length=10, choices=FINACIAL_STATUS, blank=True, null=True)
    intake_choice = models.ForeignKey(StudentIntake,on_delete=models.SET_NULL,null=True,blank=True, related_name="student_intake")


    student_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True, related_name="student_user")

    assign_university = models.ForeignKey(University,on_delete=models.SET_NULL, null=True,blank=True, related_name="assign_university")
    
    

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="student_assigned_to")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_updated_by',blank=True,null=True)
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']    

@receiver(models.signals.post_delete, sender=StudentDetail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)

@receiver(models.signals.pre_save, sender=StudentDetail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False    


class StudentDocuments(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name="student_document")
    passport = models.FileField(upload_to='documents', blank=True, null=True)
    academic_transcript = models.FileField(upload_to='documents', blank=True, null=True)
    ielts = models.FileField(upload_to='documents', blank=True, null=True)
    cv = models.FileField(upload_to='documents', blank=True, null=True)
    resume = models.FileField(upload_to='documents', blank=True, null=True)
    reference = models.FileField(upload_to='documents', blank=True, null=True)
    work_experience = models.FileField(upload_to='documents', blank=True, null=True)
    visa = models.FileField(upload_to = 'documents', blank=True, null=True)
    application_screenshot = models.FileField(upload_to='documents', blank=True, null=True)
    other = models.FileField(upload_to='documents', blank=True, null=True)
    payment_receipt = models.FileField(upload_to='documents', blank=True, null=True)
    application_form = models.FileField(upload_to='documents', blank=True, null=True)
    citizenship = models.FileField(upload_to='documents', blank=True, null=True)
    university_bank_details = models.FileField(upload_to='documents', blank=True, null=True)
    financial_documents = models.FileField(upload_to='documents', blank=True, null=True)
    medical = models.FileField(upload_to='documents', blank=True, null=True)
    vfs_appointment_booking = models.FileField(upload_to='documents', blank=True, null=True)
    ukvi_checklist = models.FileField(upload_to='documents', blank=True, null=True)
    cover_letter = models.FileField(upload_to='documents', blank=True, null=True)
    cas_statement = models.FileField(upload_to='documents', blank=True, null=True)
    birth_certificate = models.FileField(upload_to='documents', blank=True, null=True)
    sop = models.FileField(upload_to='documents', blank=True, null=True)
    sop_2 = models.FileField(upload_to='documents', blank=True, null=True)
    sop_3 = models.FileField(upload_to='documents', blank=True, null=True)
    sop_4 = models.FileField(upload_to='documents', blank=True, null=True)
    offer_letter = models.FileField(upload_to='documents', blank=True, null=True)
    offer_letter_2 = models.FileField(upload_to='documents', blank=True, null=True)
    offer_letter_3 = models.FileField(upload_to='documents', blank=True, null=True)
    offer_letter_4 = models.FileField(upload_to='documents', blank=True, null=True)

    processing_payment_receipt = models.FileField(upload_to='documents', blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_document_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_document_updated_by',blank=True,null=True)

    # def __str__(self):
    #     return self.student.name
class MultipleSop(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name='multiple_sop')
    student_document = models.ForeignKey(StudentDocuments,on_delete=models.SET_NULL,null=True,related_name='student_document_multiple_sop')
    sop = models.FileField(upload_to='documents',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sop_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sop_updated_by',blank=True,null=True)

    # def __str__(self):
    #     return self.student.name

class MultipleOfferLetter(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name='multiple_offer_letter')
    student_document = models.ForeignKey(StudentDocuments,on_delete=models.SET_NULL,null=True,related_name='student_document_multiple_offer')
    offer_letter = models.FileField(upload_to='documents',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='offer_letter_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='offer_letter_updated_by',blank=True,null=True)

    # def __str__(self):
    #     return self.student.name


class DependentDocument(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name='dependent_document')
    evidence_of_marriage = models.FileField(upload_to='documents', blank=True, null=True)
    relationship_certificate = models.FileField(upload_to='documents', blank=True, null=True)
    marriage_certificate = models.FileField(upload_to='documents', blank=True, null=True)
    dependent_passport = models.FileField(upload_to='documents', blank=True, null=True)
    dependent_medical = models.FileField(upload_to='documents', blank=True, null=True)
    dependent_cover_letter = models.FileField(upload_to='documents', blank=True, null=True)
    invitation_letter = models.FileField(upload_to='documents', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dependent_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dependent_updated_by',blank=True,null=True)

    # def __strt__(self):
    #     return self.student.name

class ChildDependentDocument(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name='child_dependent')
    child_passport = models.FileField(upload_to='documents', blank=True, null=True)
    child_birth_certificate = models.FileField(upload_to='documents', blank=True, null=True)
    child_relationship_certificate = models.FileField(upload_to='documents', blank=True, null=True)
    child_invitation_letter = models.FileField(upload_to='documents', blank=True, null=True)
    child_affidavit_letter = models.FileField(upload_to='documents', blank=True, null=True)
    child_consent_letter = models.FileField(upload_to='documents', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='child_dependent_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='child_dependent_updated_by',blank=True,null=True)

    # def __strt__(self):
    #     return self.student.name


class StudentComment(models.Model):
    student = models.ForeignKey(StudentDetail,on_delete=models.SET_NULL,null=True,related_name="student_comment")
    comments = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_created_by',blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_updated_by',blank=True,null=True)

    # def save(self,*args,**kwargs):
    #     Notification.objects.create(student_comment=self.studentcomment,student_detail=self.studentcomment.student)
    #     super(StudentComment,self).save(*args,**kwargs)

    def __str__(self):
        return self.comments

    class Meta:
        ordering = ['-created_at']


# class Student(models.Model):

#     GENDER_CHOICES=[
#         ('Male','Male'),
#         ('Female','Female'),
#         ('Other','Other'),
#     ]
#     LEVEL_CHOICES=[
#         ('Undergraduate','Undergraduate'),
#         ('Postgraduate','Postgraduate'),
#         ('Phd','Phd'),
#     ]
#     STATUS_CHOICES=[
#         ('File Not Submitted', 'File Not Submitted'),
#         ('File Submitted','File Submitted'),
#         ('Conditional Offer','Conditional Offer'),
#         ('Unconditional Offer','Unconditional Offer'),
#         ('Offer rejected','Offer rejected'),
#         ('Deposit Paid','Deposit Paid'),
#         ('Interview','Interview'),
#         ('CAS Requested','CAS Requested'),
#         ('CAS Issued','CAS Issued'),
#         ('VFS Appointment','VFS Appointment'),
#         ('Visa Granted','Visa Granted'),
#         ('Visa Rejected','Visa Rejected'),
#         ('Enrolled','Enrolled'),
#     ]
#     DEPENDENT_CHOICES=[
#         ('Yes','Yes'),
#         ('No','No'),
#     ]

#     name = models.CharField(max_length=100, blank=False)
#     profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
#     actual_email = models.EmailField(blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     password = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     dob = models.DateField(blank=True, null=True)
#     address = models.CharField(max_length=200, blank=True, null=True)
#     gender = models.CharField(max_length=200, choices=GENDER_CHOICES, blank=True, null=True)
#     academic = models.CharField(max_length=200, blank=True, null=True)
#     percentage = models.CharField(max_length=10, blank=True, null=True)
#     english = models.CharField(max_length=30, blank=True, null=True) 
#     intake = models.CharField(max_length=50, blank=True, null=True)
#     level = models.CharField(max_length=50, choices=LEVEL_CHOICES,blank=True, null=True)
#     dependent = models.CharField(max_length=50, choices=DEPENDENT_CHOICES,blank=True, null=True)
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
#     university = models.CharField(max_length=200, blank=True, null=True)
#     course = models.CharField(max_length=200, blank=True, null=True)
#     amount_paid = models.CharField(max_length=20, blank=True, null=True)
#     passport_number = models.CharField(max_length=20, blank=True, null=True)
#     recommendation = models.CharField(max_length=50, blank=True, null=True)
#     remarks = models.CharField(max_length=500, blank=True, null=True)
#     passport = models.FileField(upload_to='documents', blank=True, null=True)
#     academic_transcript = models.FileField(upload_to='documents', blank=True, null=True)
#     ielts = models.FileField(upload_to='documents', blank=True, null=True)
#     sop = models.FileField(upload_to='documents', blank=True, null=True)
#     cv = models.FileField(upload_to='documents', blank=True, null=True)
#     resume = models.FileField(upload_to='documents', blank=True, null=True)
#     reference = models.FileField(upload_to='documents', blank=True, null=True)
#     work_experience = models.FileField(upload_to='documents', blank=True, null=True)
#     visa = models.FileField(upload_to = 'documents', blank=True, null=True)
#     application_screenshot = models.FileField(upload_to='documents', blank=True, null=True)
#     other = models.FileField(upload_to='documents', blank=True, null=True)
#     payment_receipt = models.FileField(upload_to='documents', blank=True, null=True)
#     application_form = models.FileField(upload_to='documents', blank=True, null=True)
#     citizenship = models.FileField(upload_to='documents', blank=True, null=True)
#     offer_letter = models.FileField(upload_to='documents', blank=True, null=True)
#     university_bank_details = models.FileField(upload_to='documents', blank=True, null=True)
#     financial_documents = models.FileField(upload_to='documents', blank=True, null=True)
#     medical = models.FileField(upload_to='documents', blank=True, null=True)
#     vfs_appointment_booking = models.FileField(upload_to='documents', blank=True, null=True)
#     ukvi_checklist = models.FileField(upload_to='documents', blank=True, null=True)
#     relationship_certificate = models.FileField(upload_to='documents', blank=True, null=True)
#     dependent_passport = models.FileField(upload_to='documents', blank=True, null=True)
#     marriage_certificate = models.FileField(upload_to='documents', blank=True, null=True)
#     evidence_of_marriage = models.FileField(upload_to='documents', blank=True, null=True)
#     cover_letter = models.FileField(upload_to='documents', blank=True, null=True)
#     dependent_medical = models.FileField(upload_to='documents', blank=True, null=True)
#     cas_statement = models.FileField(upload_to='documents', blank=True, null=True)
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_test_created_by',blank=True, null=True)
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_test_updated_by',blank=True,null=True)
    

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ['-created_at']    

# @receiver(models.signals.post_delete, sender=Student)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.profile_image:
#         if os.path.isfile(instance.profile_image.path):
#             os.remove(instance.profile_image.path)

#     if instance.visa:
#         if os.path.isfile(instance.visa.path):
#             os.remove(instance.visa.path)

#     if instance.passport:
#         if os.path.isfile(instance.passport.path):
#             os.remove(instance.passport.path)

#     if instance.academic_transcript:
#         if os.path.isfile(instance.academic_transcript.path):
#             os.remove(instance.academic_transcript.path)

#     if instance.ielts:
#         if os.path.isfile(instance.ielts.path):
#             os.remove(instance.ielts.path)

#     if instance.sop:
#         if os.path.isfile(instance.sop.path):
#             os.remove(instance.sop.path)                                        

#     if instance.resume:
#         if os.path.isfile(instance.resume.path):
#             os.remove(instance.resume.path)

#     if instance.reference:
#         if os.path.isfile(instance.reference.path):
#             os.remove(instance.reference.path)

#     if instance.work_experience:
#         if os.path.isfile(instance.work_experience.path):
#             os.remove(instance.work_experience.path)        

#     if instance.application_screenshot:
#         if os.path.isfile(instance.application_screenshot.path):
#             os.remove(instance.application_screenshot.path)

#     if instance.other:
#         if os.path.isfile(instance.other.path):
#             os.remove(instance.other.path)        

#     if instance.payment_receipt:
#         if os.path.isfile(instance.payment_receipt.path):
#             os.remove(instance.payment_receipt.path)  

#     if instance.citizenship:
#         if os.path.isfile(instance.citizenship.path):
#             os.remove(instance.citizenship.path)   

#     if instance.offer_letter:
#         if os.path.isfile(instance.offer_letter.path):
#             os.remove(instance.offer_letter.path)  

#     if instance.university_bank_details:
#         if os.path.isfile(instance.university_bank_details.path):
#             os.remove(instance.university_bank_details.path) 
    
#     if instance.financial_documents:
#         if os.path.isfile(instance.financial_documents.path):
#             os.remove(instance.financial_documents.path)
    
#     if instance.medical:
#         if os.path.isfile(instance.medical.path):
#             os.remove(instance.medical.path)
    
#     if instance.vfs_appointment_booking:
#         if os.path.isfile(instance.vfs_appointment_booking.path):
#             os.remove(instance.vfs_appointment_booking.path)

#     if instance.ukvi_checklist:
#         if os.path.isfile(instance.ukvi_checklist.path):
#             os.remove(instance.ukvi_checklist.path)

#     if instance.relationship_certificate:
#         if os.path.isfile(instance.relationship_certificate.path):
#             os.remove(instance.relationship_certificate.path)
    
#     if instance.dependent_passport:
#         if os.path.isfile(instance.dependent_passport.path):
#             os.remove(instance.dependent_passport.path)

#     if instance.marriage_certificate:
#         if os.path.isfile(instance.marriage_certificate.path):
#             os.remove(instance.marriage_certificate.path)
    
#     if instance.evidence_of_marriage:
#         if os.path.isfile(instance.evidence_of_marriage.path):
#             os.remove(instance.evidence_of_marriage.path)
    
#     if instance.cover_letter:
#         if os.path.isfile(instance.cover_letter.path):
#             os.remove(instance.cover_letter.path)
   
#     if instance.cas_statement:
#         if os.path.isfile(instance.cas_statement.path):
#             os.remove(instance.cas_statement.path)

# @receiver(models.signals.pre_save, sender=Student)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False



