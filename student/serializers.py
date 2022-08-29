from rest_framework import serializers
from notification.models import Notification
import student

from student.models import ChildDependentDocument, DependentDocument, StudentIntake,MultipleOfferLetter, MultipleSop, StudentComment, StudentDetail, StudentDocuments, University
from user.serializers import UserSerializer
from user.models import User



class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields='__all__'


class StudentIntakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentIntake
        fields=['id','name','is_active']       

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class MultipleSopSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleSop
        fields = ['id','student','sop']
        read_only_fields=['created_at','updated_at','sop_created_by','sop_updated_by']
  

class MultipleOfferLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleOfferLetter
        fields = "__all__"    
        read_only_fields=['created_at','updated_at','offer_letter_created_by','offer_letter_updated_by']    

class DependentDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DependentDocument
        fields = "__all__"
        read_only_fields=['created_at','updated_at','dependent_created_by','dependent_updated_by']

class ChildDependentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildDependentDocument
        fields = '__all__'
        read_only_fields=['created_at','updated_at','child_dependent_created_by','child_dependent_updated_by']


class StudentDocumentSerializer(serializers.ModelSerializer):
    student_document_multiple_sop = MultipleSopSerializer(many=True,required=False)
    # student_id = serializers.CharField(required=False)
    student_document_multiple_offer = MultipleOfferLetterSerializer(many=True,required=False)
    class Meta:
        model = StudentDocuments
        fields = ["id","passport","academic_transcript","ielts","cv","resume","reference","work_experience","visa","application_screenshot","other","payment_receipt","application_form","citizenship","university_bank_details","financial_documents",
                    "medical","vfs_appointment_booking","ukvi_checklist","cover_letter","cas_statement","birth_certificate","sop","sop_2","sop_3","sop_4","offer_letter","offer_letter_2","offer_letter_3","offer_letter_4",'student_document_multiple_sop',
                    "student_document_multiple_offer",'student','processing_payment_receipt']

    def create(self, validated_data):
        user = self.context['request'].user

        images_data = self.context['request'].FILES.getlist('multiple_sop')
        multiple_offer = self.context['request'].FILES.getlist('multiple_offer')
        student_document = StudentDocuments.objects.create(**validated_data)
        student = validated_data.get('student')

        # student_data = Student.objects.get(id=student)
        # print(student_data)

          
 
        if images_data: 
            for image in images_data:
                MultipleSop.objects.create(student=student,student_document=student_document, sop=image,created_by=user)
        if multiple_offer:
            for offer in multiple_offer:
                MultipleOfferLetter.objects.create(student=student,student_document=student_document, offer_letter=offer,created_by=user)    
        return student_document 

    # def update(self, instance, validated_data):
        # images_data = self.context['request'].FILES.getlist('multiple_sop')
        # sop_id = validated_data.get('sop_id')
        # print("sop",sop_id)
        # images = instance.multiple_sop.all()
        # images = list(images)
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()
        # for image_data in images_data:
        #     print(image_data,"hello")
        #     image = images.pop(0)
        #     image.sop = image_data
        #     image.save()
        # return instance        

class StudentCommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    updated_by = UserSerializer()

    class Meta:
        model = StudentComment
        fields = ['id','comments','student','created_at','updated_at','created_by','updated_by']

class StudentCommentCreateSerializer(serializers.ModelSerializer):
    # created_by = UserSerializer()
    # updated_by = UserSerializer()

    class Meta:
        model = StudentComment
        fields = ['id','comments','student']
        read_only_fields=['created_by','updated_by']

    def create(self, validated_data):
        # student  = self.context['request'].get("student")
        student_comment = StudentComment.objects.create(**validated_data)
        Notification.objects.create(student_comment=student_comment,student_detail=student_comment.student)
        return student_comment    

class StudentCreateSerializer(serializers.ModelSerializer):
    gender = ChoiceField(choices=StudentDetail.GENDER_CHOICES,required=False)
    level = ChoiceField(choices=StudentDetail.LEVEL_CHOICES,required=False)
    status = ChoiceField(choices=StudentDetail.STATUS_CHOICES,required=False)
    dependent = ChoiceField(choices=StudentDetail.DEPENDENT_CHOICES,required=False)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = StudentDetail
        fields = [
            "id",
            "name",
            "profile_image",
            "actual_email",
            "email",
            "password",
            "phone",
            "dob",
            "address",
            "gender",
            "academic",
            "percentage",
            "english",
            "intake",
            "level",
            "dependent",
            "status",
            "university",
            "course",
            "amount_paid",
            "passport_number",
            "recommendation",
	        "remarks",
            "email_access",
            "financial_status",
            "student_user",
            "assigned_to",
            "assign_university",
            "intake_choice"
        ]
        read_only_fields=['created_at','updated_at','created_by','updated_by']      

class StudentSerializer(StudentCreateSerializer):
    assigned_to = UserSerializer()
    created_by=UserSerializer()
    updated_by=UserSerializer()
    # multiple_sop = MultipleSopSerializer(many=True)
    # multiple_offer_letter = MultipleOfferLetterSerializer(many=True)
    child_dependent =  serializers.SerializerMethodField()
    dependent_document =  serializers.SerializerMethodField()
    student_comment =  serializers.SerializerMethodField()
    student_document = serializers.SerializerMethodField()
    assign_university=UniversitySerializer()
    intake_choice = StudentIntakeSerializer()

    class Meta(StudentCreateSerializer.Meta):
        fields = StudentCreateSerializer.Meta.fields + ['intake_choice','student_document','child_dependent','dependent_document','student_comment','created_by','updated_by','assigned_to','assign_university']

    def get_student_document(self,obj):
        a = StudentDocuments.objects.filter(student_id=obj.id)
        serializer = StudentDocumentSerializer(a,many=True)
        return serializer.data

    def get_student_comment(self,obj):
        a = StudentComment.objects.filter(student_id=obj.id)
        serializer = StudentCommentSerializer(a,many=True)
        notification =""
        if 'notification_id' in self.context['request'].data:
            notification = self.context['request'].data['notification_id']
        if notification:
            seen_notification = Notification.objects.get(id=notification)
            seen_notification.is_seen = True
            seen_notification.save()
        return serializer.data

    def get_dependent_document(self,obj):
        a = DependentDocument.objects.filter(student_id=obj.id)
        serializer = DependentDocumentSerializer(a,many=True)
        return serializer.data

    def get_child_dependent(self,obj):
        a = ChildDependentDocument.objects.filter(student_id=obj.id)
        serializer = ChildDependentSerializer(a,many=True)
        return serializer.data    

    def get_assigned_to(self,obj):
        print(obj)
        a = User.objects.get(id=obj.assigned_to)
        serializer = UserSerializer(a)
        return serializer.data
    
    def get_notification_change(self,obj):
        notification = self.context['request'].data['notification_id']
        print("notification",notification)

    # def get_intake(self,obj):
    #     print(obj)
    #     a = StudentIntake.objects.filter(id=obj.intake)
    #     serializer = StudentIntakeSerializer(a,many=True)
    #     return serializer.data    

