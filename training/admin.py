from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(ThreatAlert)
admin.site.register(EducationalResource)
admin.site.register(UserProfile)
admin.site.register(TrainingModule)
# admin.site.register(UserProgress)
admin.site.register(UserAlert)

from .models import ThreatAlert, TrainingModule, UserProgress, EducationalResource, UserProfile, TrainingModule, UserAlert, ModuleContent


@admin.register(ThreatAlert)
class ThreatAlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'threat_level', 'date_posted']  # Changed 'severity' to 'threat_level', 'created_at' to 'date_posted'
    list_filter = ['threat_level', 'is_active']  # Changed 'severity' to 'threat_level'
    search_fields = ['title', 'description']
    readonly_fields = ['date_posted']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'module', 'completed', 'completion_date']  # Removed 'last_accessed'
    list_filter = ['completed', 'module']
    search_fields = ['user__username', 'module__title']