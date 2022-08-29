from django.contrib import admin
from student.models import StudentDetail, MultipleOfferLetter, MultipleSop, DependentDocument, ChildDependentDocument, StudentComment, StudentDocuments, StudentIntake, University

# Register your models here.

admin.site.register(MultipleOfferLetter)

admin.site.register(MultipleSop)

admin.site.register(DependentDocument)

admin.site.register(ChildDependentDocument)

admin.site.register(StudentDocuments)

admin.site.register(StudentComment)

admin.site.register(StudentDetail)

admin.site.register(University)

admin.site.register(StudentIntake)