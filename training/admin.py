from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(ThreatAlert)
admin.site.register(EducationalResource)
admin.site.register(UserProfile)
admin.site.register(TrainingModule)
# admin.site.register(UserProgress)
admin.site.register(UserAlert)

from .models import ThreatAlert, TrainingModule, UserProgress

@admin.register(ThreatAlert)
class ThreatAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'created_at', 'is_active')
    list_filter = ('severity', 'is_active')
    search_fields = ('title', 'description')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'completed', 'last_accessed')
    list_filter = ('completed', 'module')
    search_fields = ('user__username', 'module__title')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'module')