from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, 'Title must be greater than 2 characters')]
    )
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(
        max_length=256,
        null=True,
        help_text='The MIMEType of the file'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
