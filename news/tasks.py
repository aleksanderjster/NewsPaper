from celery import shared_task
import os
from .models import Post, Category
from django.conf import settings
from django.core.mail import send_mail
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()



@shared_task
def NewPostNotificationTask(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.category.all()
    for category in categories:

        subscriber_email_list = []
        subscribers = category.subscriber.all()
        for subscriber in subscribers:
            subscriber_email_list.append(subscriber.email)
        
        send_notification(post=post,category=category, subscriber_email_list=subscriber_email_list)
    
    print('INFO: End of NewPostNotificationTask')



def send_notification(post, category, subscriber_email_list):
    
    # composing the e-mail content
    notification_subject = f'New post added in {category} you subscribed on'
    notification_body = f'New post "{post.title}" published.\n'
    notification_body += f'\n\n{post.preview()}\n'
    notification_body += f'\n Follow link: {settings.SITE_URL}{post.get_absolute_url()}'

    # sending mail
    send_mail(notification_subject, 
              notification_body,
              os.getenv('DEFAULT_EMAIL'),
              subscriber_email_list,
              fail_silently=False)
    
@shared_task
def WeekNewsNotification():
  
    # Your job processing logic here...

    # TODO:

    # 1. form news_list from news for the defined period (1 week)
    current_date = datetime.now() # this is date when task triggered
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
        # print(email_body)
        # print(f"send to: {category_subscriber_emails}")
        send_mail(
          email_subject, 
          email_body,
          os.getenv('DEFAULT_EMAIL'),
          category_subscriber_emails,
          fail_silently=False
        )
