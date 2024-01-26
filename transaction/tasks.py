from celery import shared_task
from billy.models import Profile


@shared_task
def add_monthly_members_points():
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.points = 500
        profile.save()
