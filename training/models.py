from django.db import models
from django.contrib.auth.models import User

class ThreatAlert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    threat_level = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    date_posted = models.DateTimeField(auto_now_add=True)
    recommended_actions = models.TextField()

    def __str__(self):
        return self.title

class EducationalResource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    resource_type = models.CharField(max_length=50, choices=[
        ('article', 'Article'),
        ('video', 'Video'),
        ('guide', 'Guide'),
        ('checklist', 'Checklist')
    ])
    date_added = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_sector = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    subscription_active = models.BooleanField(default=True)