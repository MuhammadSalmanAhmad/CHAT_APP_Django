import logging
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message
from django.core.mail import send_mail
from django.conf import settings
#in post save reciever has arguments like created( a flag ),instance


@receiver(post_delete, sender=Message)
def message_delete_handler(sender, instance, *args, **kwargs):
    print(args,kwargs)

    print(f"Message {instance.content} has been deleted")
    
   

#post_delete.connect(message_delete_handler,sender=Message) This does the same thing as the above reciever decorator

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"User {instance.username} has been created")
        print(instance.email)
        try:

            send_mail(
            subject="Welcome to Code Suit",
            recipient_list=[instance.email],
            message=f"Hi {instance.username} welcome to code suit",
            from_email= settings.EMAIL_HOST_USER,
            fail_silently=False
        )
        except Exception as e:
            print(e)
        # Perform actions for a new user creation, e.g., sending a welcome email

    else:
        logger.info(f"User {instance.username} has been updated")
        # Perform actions for user update if necessary

@receiver(post_save,sender=Message)
def create_message_handler(sender,created,instance,*args,**kwargs):

    print(args,kwargs)
    if created:
        print(f"Message {instance.content} has been created")
    else:
        print(f"Message {instance.content} has been updated")
    return HttpResponse({
        "created": f"Message {instance.content} has been created"
    })