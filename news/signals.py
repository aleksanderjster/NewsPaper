
from .models import Post
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

# calling celery tasks from signals
from .tasks import NewPostNotificationTask



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

            NewPostNotificationTask.delay(post_id=instance.id) # calling task as async
