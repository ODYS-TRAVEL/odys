from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    airtable_agency_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'
