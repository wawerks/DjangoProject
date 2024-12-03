from django.db import models

# Create your models here.

class Message(models.Model):
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
