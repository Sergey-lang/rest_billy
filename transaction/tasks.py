from celery import shared_task


@shared_task
def add_monthly_members_points():
    return True
