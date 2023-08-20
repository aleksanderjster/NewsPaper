import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
 
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.conf.beat_schedule ={
    'weekly_news_summary_notification':{
        'task': 'news.tasks.WeekNewsNotification',
        # 'schedule': 120,
        'schedule': crontab(hour=8,
                            minute=0,
                            day_of_week='mon'),
        'args': (),
    },
}

app.autodiscover_tasks()
