from django.db import models
from django.contrib.auth.models import User

class ThreatAlert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'), 
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    threat_level = models.CharField(
        max_length=50, 
        choices=SEVERITY_CHOICES,
        default='medium'
    )
    date_posted = models.DateTimeField(auto_now_add=True)
    recommended_actions = models.TextField()
    affected_systems = models.CharField(max_length=200, blank=True)  
    is_active = models.BooleanField(default=True)  
    
    class Meta:
        ordering = ['-date_posted']
        
    def __str__(self):
        return f"{self.get_threat_level_display()}: {self.title}"

class EducationalResource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('guide', 'Guide'),
        ('checklist', 'Checklist'),
        ('quiz', 'Quiz'),  
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    resource_type = models.CharField(
        max_length=50, 
        choices=RESOURCE_TYPES
    )
    date_added = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=10)  # 
    difficulty = models.CharField(  
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.title

# Updated UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_sector = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    subscription_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)  # For progress tracking
    
    def __str__(self):
        return f"{self.user.username} - {self.business_name}"

# New models for training modules and progress tracking
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    resources = models.ManyToManyField(EducationalResource)  # Reuse existing resources
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sequence = models.PositiveIntegerField(default=0)  # For ordering modules
    
    class Meta:
        ordering = ['sequence']
        
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    resource = models.ForeignKey(EducationalResource, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    quiz_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'module', 'resource')
        verbose_name_plural = 'User progress'
        
    def __str__(self):
        return f"{self.user.username} - {self.module.title}"
    
    @property
    def time_spent(self):
        if self.completion_date and self.module.created_at:
            return (self.completion_date - self.module.created_at).total_seconds() / 60
        return 0
    
# added UserAlert model to track user interactions with alerts
class UserAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(ThreatAlert, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    notified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'alert')
        
    def __str__(self):
        return f"{self.user.username} - {self.alert.title}"
    
class ModuleContent(models.Model):
    CONTENT_TYPES = [
        ('TEXT', 'Text'),
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
    ]
    
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()  # Could be JSONField for quizzes
    sequence = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['sequence']

class UserBadge(models.Model):
    BADGE_TYPES = [
        ('completion', 'Module Completion'),
        ('speed', 'Fast Learner'),
        ('quiz', 'Quiz Master'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    awarded_date = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey(TrainingModule, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('user', 'badge_type', 'module')
 