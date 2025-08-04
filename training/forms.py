from django import forms
from .models import ThreatAlert

class ThreatAlertForm(forms.ModelForm):
    class Meta:
        model = ThreatAlert
        fields = ['title', 'description', 'severity', 'affected_systems', 'mitigation_steps']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'mitigation_steps': forms.Textarea(attrs={'rows': 4}),
        }

class ThreatAlertForm(forms.ModelForm):
    class Meta:
        model = ThreatAlert
        fields = ['title', 'description', 'threat_level', 'affected_systems', 'recommended_actions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'recommended_actions': forms.Textarea(attrs={'rows': 4}),
        }        
