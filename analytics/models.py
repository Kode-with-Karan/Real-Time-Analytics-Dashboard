from django.db import models
from django.utils import timezone

class PageView(models.Model):
    session_id = models.CharField(max_length=100)
    page_url = models.URLField()
    timestamp = models.DateTimeField(default=timezone.now)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()

class Conversion(models.Model):
    session_id = models.CharField(max_length=100)
    conversion_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True)