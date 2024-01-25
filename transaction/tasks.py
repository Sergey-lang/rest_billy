from celery import shared_task
from billy.models import Profile

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def add_monthly_members_points(*args):
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.points = 500
        profile.save()
