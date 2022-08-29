from django.db import models

from student.models import StudentComment, StudentDetail

class Notification(models.Model):
    student_comment = models.ForeignKey(StudentComment,on_delete=models.CASCADE)
    student_detail = models.ForeignKey(StudentDetail,on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']