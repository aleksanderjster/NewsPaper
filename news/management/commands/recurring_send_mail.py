import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from datetime import datetime, timedelta
from news.models import Post, Category
from django.core.mail import send_mail
import os


logger = logging.getLogger(__name__)


def weekly_news_notification():
  
    # Your job processing logic here...

    # TODO:

    # 1. form news_list from news for the defined period (1 week)
    current_date = datetime.now()
    period_days = 7
    start_date = current_date - timedelta(days=period_days)
    news_within_range = Post.objects.filter(publication_date__range=(start_date, current_date))


    # 2. form subscriber_list for every category

    for category in Category.objects.all():
        category_subscribers = category.subscriber.all()

        if len(category_subscribers) == 0: # skip on category which has no subscribers
           continue
        
        category_subscriber_emails = []
        email_body = ''
        for subscriber in category_subscribers:
            category_subscriber_emails.append(subscriber.email)
            
        # 3. find all news for this category in news_list
        category_news_set = news_within_range.filter(category=category).order_by("publication_date")

        if len(category_news_set) == 0:   # skip on category which has no news for period
           continue
        
        email_subject = f'NewsPortal: News for passed week in {category.__str__()} category.'
        email_body = '=' * 60 + f'\nList of news for passed week in {category.__str__()} category you subscribed for:\n' + '=' * 60 + '\n'
        
        for post in category_news_set:
           email_body += f'Title: "{post.title}" follow link: {settings.SITE_URL}{post.get_absolute_url()}\n'

        # 4. send email with category_news_list to the category_subscribers
        print(email_body)
        # print(f"send to: {category_subscriber_emails}")
        send_mail(
          email_subject, 
          email_body,
          os.getenv('DEFAULT_EMAIL'),
          category_subscriber_emails,
          fail_silently=False
        )
  



# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      weekly_news_notification,
      trigger=CronTrigger(day="*/7"),  # Every 1 minute
      id="weekly_news_notification",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'weekly_news_notification'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")