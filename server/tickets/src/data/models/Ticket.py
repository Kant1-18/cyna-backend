from django.db import models
from users.models import User


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.IntegerField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
