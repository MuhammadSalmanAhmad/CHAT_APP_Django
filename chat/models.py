# Remove the duplicate import statement

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(User, related_name='chats')

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=255)
    

class Message(models.Model):
    #chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    group= models.ForeignKey(ChatGroup,on_delete=models.CASCADE,related_name='chat_groups')
   
#Additionaly these models can be incorporated 

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    status = models.CharField(max_length=100, blank=True)


class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

"""