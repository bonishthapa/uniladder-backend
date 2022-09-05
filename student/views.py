from django.shortcuts import render
from rest_framework import viewsets, generics
from django.http import HttpResponse
from notification.models import Notification
from student import serializers
from student.models import ChildDependentDocument, DependentDocument, MultipleOfferLetter, MultipleSop, StudentComment, StudentDetail, StudentDocuments, StudentIntake, University
from student.serializers import ChildDependentSerializer, StudentIntakeSerializer , DependentDocumentSerializer, MultipleOfferLetterSerializer, MultipleSopSerializer, StudentCommentCreateSerializer, StudentCommentSerializer, StudentCreateSerializer, StudentDocumentSerializer, StudentSerializer, UniversitySerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from student.paginations import StudentPaginaition

from user.models import User
from user.serializers import UserSerializer
import csv
# Create your views here.

class StudentAPIView(viewsets.ModelViewSet):
    queryset = StudentDetail.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['financial_status','gender','level','assigned_to','status','intake_choice','assign_university']
    search_fields = ['name']
    pagination_class = StudentPaginaition

    def get_queryset(self):
        if self.request.user.is_admin:
            queryset = StudentDetail.objects.all()
        elif self.request.user.role == "Admin":
            queryset = StudentDetail.objects.all()
        elif self.request.user.role == "Student":
            queryset = StudentDetail.objects.filter(student_user=self.request.user)
        else:    
            queryset = StudentDetail.objects.filter(assigned_to=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentCreateSerializer
        elif self.action == 'update':    
            return StudentCreateSerializer    
        elif self.action == 'partial_update':    
            return StudentCreateSerializer
        else:
            return StudentSerializer        

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        if request.GET:
            amount_pay = request.GET.get('amount_paid',None)
            if amount_pay:
                if amount_pay == 'Unpaid':
                    querysetData = queryset.filter(Q(amount_paid__exact='')|Q(amount_paid__exact=0)|Q(amount_paid__isnull=True))
                    page = self.paginate_queryset(querysetData)
                    if page is not None:
                        serializer = self.get_serializer(page, many=True)
                        return self.get_paginated_response(serializer.data)

                    serializer = self.get_serializer(queryset, many=True)

                    return Response(serializer.data,status.HTTP_200_OK)
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)    
                return Response(serializer.data,status.HTTP_200_OK)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data,status.HTTP_200_OK)    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status.HTTP_200_OK)
       

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

class DashboardStatAPIView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self,*args, **kwargs):
        queryset = StudentDetail.objects.all()
        total_student = queryset.count()
        enrolled = queryset.filter(status="Enrolled").count()
        visa_granted = queryset.filter(status="Visa Granted").count()
        offer_pending = queryset.filter(status="Offer Pending").count()
        visa_pending = queryset.filter(status="Visa Pending").count()
        interview = queryset.filter(status="Interview").count()
        cas_pending = queryset.filter(status="CAS Requested").count()
        return Response({
            'total_student':total_student,
            'visa_granted':visa_granted,
            'enrolled':enrolled,
            'offer_pending':offer_pending,
            'visa_pending':visa_pending,
            'interview':interview,
            'cas_pending':cas_pending,
            })

class MultipleSopView(viewsets.ModelViewSet):
    queryset = MultipleSop.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MultipleSopSerializer
    
    
    # def create(self, request, **kwargs):
    #     if self.request.user.is_active:
    #         print(request.data)
    #         serializer = self.get_serializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(created_by=request.user)
    #             return Response(serializer.data, status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors)
             

    # def update(self, request, **kwargs):
    #     if self.request.user.is_active:
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #         if serializer.is_valid():
    #             serializer.save(updated_by=request.user)
    #             return Response(serializer.data, status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors)

    def destroy(self,request,pk=None):
        return Response({"detail":"Delete Method is not allowded"},status=status.HTTP_200_OK)

class StudentDocumentView(viewsets.ModelViewSet):
    queryset = StudentDocuments.objects.all()
    permission_classes =(IsAuthenticated,)
    serializer_class = StudentDocumentSerializer

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
        sop_id = ""
        offer_id = ""
        if 'sop_id' in request.data:
            sop_id = request.data['sop_id']

        if 'offer_id' in request.data:    
            offer_id = request.data['offer_id']
        img_offer = request.FILES.get('multiple_offer')
        img_sop = request.FILES.get('multiple_sop')
        if self.request.user.is_active:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                if sop_id:
                    sop = MultipleSop.objects.get(id=sop_id)
                    sop.sop = img_sop
                    sop.save()
                else:
                    if img_sop:
                        MultipleSop.objects.create(offer_letter = img_sop,student_document = instance)    
                     
                if offer_id:
                    offer = MultipleOfferLetter.objects.get(id=offer_id)
                    offer.offer_letter = img_offer
                    offer.save()
                else:
                    if img_offer:
                        MultipleOfferLetter.objects.create(offer_letter = img_offer,student_document = instance)  

                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)       
        return Response({"Error": "User is not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

class MultipleOfferLetterView(viewsets.ModelViewSet):
    queryset = MultipleOfferLetter.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MultipleOfferLetterSerializer
    

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

    def destroy(self,request,pk=None):
        return Response({"detail":"Delete Method is not allowded"},status=status.HTTP_200_OK)            

class DependentDocumentView(viewsets.ModelViewSet):
    queryset = DependentDocument.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DependentDocumentSerializer
    

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


    def destroy(self,request,pk=None):
        return Response({"detail":"Delete Method is not allowded"},status=status.HTTP_200_OK)            

class ChildeDocumentView(viewsets.ModelViewSet):
    queryset = ChildDependentDocument.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChildDependentSerializer
    

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


    def destroy(self,request,pk=None):
        return Response({"detail":"Delete Method is not allowded"},status=status.HTTP_200_OK)

class StudentCommentView(viewsets.ModelViewSet):
    queryset = StudentComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentCommentSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return StudentCommentSerializer
        elif self.action == "retrieve":
            return StudentCommentSerializer    
        else:
            return StudentCommentCreateSerializer

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
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        return Response({"Error": "User is not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)   



# def get_all(request):
#     queryset = Student.objects.all()
#     print(queryset)
#     for i in queryset:
#         a=StudentDetail.objects.create(
#             name = i.name,
#             profile_image = i.profile_image,
#             actual_email = i.actual_email,
#             email = i.email,
#             password = i.password,
#             phone = i.phone,
#             dob = i.dob,
#             address = i.address,
#             gender = i.gender,
#             academic = i.academic,
#             percentage =i.percentage,
#             english = i.english,
#             intake =i.intake,
#             level =i.level,
#             dependent =i.dependent,
#             status =i.status,
#             university =i.university,
#             course =i.course,
#             amount_paid =i.amount_paid,
#             passport_number=i.passport_number,
#             recommendation=i.recommendation,
#             remarks=i.remarks,
#             )
#         if a.id:
#             StudentDocuments.objects.create(
#             student = a,
#             passport = i.passport,
#             academic_transcript = i.academic_transcript,
#             ielts = i.ielts,
#             cv = i.cv,
#             resume = i.resume,
#             reference = i.reference,
#             work_experience = i.work_experience,
#             visa = i.visa,
#             application_screenshot = i.application_screenshot,
#             other = i.other,
#             payment_receipt = i.payment_receipt,
#             application_form = i.application_form,
#             citizenship = i.citizenship,
#             university_bank_details = i.university_bank_details,
#             financial_documents = i.financial_documents,
#             medical = i.medical,
#             vfs_appointment_booking = i.vfs_appointment_booking,
#             ukvi_checklist = i.ukvi_checklist,
#             cover_letter = i.cover_letter,
#             cas_statement = i.cas_statement,
#             sop = i.sop,
#             offer_letter = i.offer_letter,
#         )   
#     return HttpResponse("done")

class UniversityApiView(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StudentPaginaition
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

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

class StudentSelfDataAPI(viewsets.ModelViewSet):
    serializer_class=StudentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self,*args,**kwargs):
        queryset=StudentDetail.objects.filter(student_user=self.request.user)
        return queryset


class ExportStudentExcelAPI(generics.GenericAPIView):
    queryset = StudentDetail.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['financial_status','gender','level','assigned_to','status']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if self.request.user.is_admin or self.request.user.role == "Admin":
            print("hello",self.filter_queryset(self.get_queryset()))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users.csv"'

            writer = csv.writer(response)
            writer.writerow(["name","actual_email","email","password","phone","dob","address","gender","academic","percentage","english","intake","level","dependent","status","university","course","amount_paid","passport_number","recommendation","remarks","email_access","financial_status","assign_university","assigned_to","created_at","updated_at","created_by","updated_by"])

            users = self.filter_queryset(self.get_queryset()).values_list("name","actual_email","email","password","phone","dob","address","gender","academic","percentage","english","intake","level","dependent","status","university","course","amount_paid","passport_number","recommendation","remarks","email_access","financial_status","assign_university__name","assigned_to__email","created_at","updated_at","created_by__email","updated_by__email")
            for user in users:
                writer.writerow(user)

            return response
        else:    
            return Response({"detail":"Authenticated User not Found"},status=status.HTTP_401_UNAUTHORIZED)


class IntakeApiView(generics.ListAPIView):
    queryset = StudentIntake.objects.filter(is_active=True)      
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentIntakeSerializer
