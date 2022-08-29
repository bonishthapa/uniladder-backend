from rest_framework import generics
from notification.serializers import NotificationSerializer

from student.paginations import StudentPaginaition
from rest_framework.permissions import IsAuthenticated
from notification.models import Notification


# Create your views here.

class NotificationApi(generics.ListAPIView):
    model = Notification
    # queryset = Notification.objects.filter(student_detail__student_user=request.user)      
    permission_classes = (IsAuthenticated,)
    pagination_class = StudentPaginaition
    serializer_class = NotificationSerializer

    def get_queryset(self):
        notification = Notification.objects.filter(student_detail__assigned_to=self.request.user)
        return notification