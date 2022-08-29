from rest_framework import serializers
from notification.models import Notification
from student.serializers import StudentCommentSerializer, StudentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer()
    student_comment = StudentCommentSerializer()

    class Meta:
        model = Notification
        fields = ['id','student_detail','student_comment','is_seen','created_at','updated_at']

    def conversion_bool(self, instance):
        if instance.is_seen == True:
            return "Down"
        else:
            return "Up"