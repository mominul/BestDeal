from django.db import models

# Create your models here.
class ChatHistory(models.Model):
    prompt = models.TextField()
    response = models.TextField()

    def __str__(self) -> str:
        return self.prompt
