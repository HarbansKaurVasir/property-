from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # Define the upload_to path as needed

    def __str__(self):
        return self.name