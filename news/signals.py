import os

from .models import Post
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from dotenv import load_dotenv
from django.conf import settings
load_dotenv()



@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, **kwargs):
    if sender.type == 'A':      # Letters should be send for news only.
        return
    
    if created:
        # Handle post_save for newly created posts here
        instance._is_new = True


@receiver(m2m_changed, sender=Post.category.through)
def m2m_changed_handler(sender, instance, action, **kwargs): # instance is the added Post object
    if action == "post_add":
        # Check if the instance-level variable is True (indicating a new post)
        if getattr(instance, "_is_new", False) and instance.category.exists():
            # Both conditions met: New post created and category added"
            delattr(instance, "_is_new")  # Remove the flag once checked

            categories = instance.category.all()
            for category in categories:

                subscriber_email_list = []
                subscribers = category.subscriber.all()
                for subscriber in subscribers:
                    subscriber_email_list.append(subscriber.email)
                
                send_notification(post=instance,category=category, subscriber_email_list=subscriber_email_list)


def send_notification(post, category, subscriber_email_list):
    import time
    print('INFO: start sending notifications')
    time.sleep(60)
    print('INFO:  notifications are sent')
    
    # # composing the e-mail content
    # notification_subject = f'New post added in {category} you subscribed on'
    # notification_body = f'New post "{post.title}" published.\n'
    # notification_body += f'\n\n{post.preview()}\n'
    # notification_body += f'\n Follow link: {settings.SITE_URL}{post.get_absolute_url()}'

    # # sending mail
    # send_mail(notification_subject, 
    #           notification_body,
    #           os.getenv('DEFAULT_EMAIL'),
    #           subscriber_email_list,
    #           fail_silently=False)
