from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProgress, UserBadge

@receiver(post_save, sender=UserProgress)
def award_badges(sender, instance, created, **kwargs):
    if instance.completed:
        user = instance.user
        module = instance.module
        
        # Completion Badge
        if not UserBadge.objects.filter(user=user, badge_type='completion', module=module).exists():
            UserBadge.objects.create(user=user, badge_type='completion', module=module)
        
        # Fast Learner Badge (completed in < 30 min)
        if instance.time_spent < 30:
            if not UserBadge.objects.filter(user=user, badge_type='speed', module=module).exists():
                UserBadge.objects.create(user=user, badge_type='speed', module=module)
        
        # Quiz Master Badge (score > 90%)
        if instance.quiz_score and instance.quiz_score >= 90:
            if not UserBadge.objects.filter(user=user, badge_type='quiz', module=module).exists():
                UserBadge.objects.create(user=user, badge_type='quiz', module=module)