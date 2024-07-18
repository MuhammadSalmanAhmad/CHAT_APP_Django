from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Chat, Message,ChatGroup

# Register your models here.
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatGroup)