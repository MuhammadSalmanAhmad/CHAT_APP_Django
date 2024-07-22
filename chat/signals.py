from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message
#in post save reciever has arguments like created( a flag ),instance


@receiver(post_delete, sender=Message)
def message_delete_handler(sender, instance, *args, **kwargs):
    print(args,kwargs)

    print(f"Message {instance.content} has been deleted")
    
   

#post_delete.connect(message_delete_handler,sender=Message) This does the same thing as the above reciever decorator

@receiver(post_save,sender=User)
def user_created_handler(sender,created,instance,*args,**kwargs):
    print(args,kwargs)
    User.objects.create(instance)
    if created:
        print(f"User {instance.username} has been created")
    else:
        print(f"User {instance.username} has been updated")
    return HttpResponse({
        "created": f"User {instance.username} has been created"
    })

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