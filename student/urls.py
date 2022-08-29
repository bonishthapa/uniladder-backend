from django.urls import path,include
from rest_framework.routers import DefaultRouter
from student import views

router = DefaultRouter()

router.register('student', views.StudentAPIView, basename='student')
router.register('student-detail/multiple-sop', views.MultipleSopView, basename='multiplesop')
router.register('student-detail/multiple-offer-letter', views.MultipleOfferLetterView, basename='multiplesoffetletter')
router.register('student-detail/dependent-document', views.DependentDocumentView, basename='dependentdocument')
router.register('student-detail/child-document', views.ChildeDocumentView, basename='childdocument')
router.register('student-detail/student-document', views.StudentDocumentView, basename='childdocument')
router.register('student-detail/comment', views.StudentCommentView, basename="studentcomment")
router.register('university', views.UniversityApiView, basename="studentcomment")
router.register('detail/student', views.StudentSelfDataAPI, basename="student-detail")



# router.register('dashboard/stat', views.DashboardStatAPIView, basename='stat')


urlpatterns = [
    path('api/',include(router.urls)),
    path('api/dashboard/stat/', views.DashboardStatAPIView.as_view({'get':'list'}), name='dashboard'),
    path('api/export/student/', views.ExportStudentExcelAPI.as_view(), name='student-export'),
    path('api/intake/student/', views.IntakeApiView.as_view(),name="student-intake"),
]