from rest_framework import serializers
from .models import Chat,Message,ChatGroup
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
    def create(self, validated_data):
        read_by_users = validated_data.pop('read_by', [])
        
        # Check if sender exists
        users = User.objects.all()
        if validated_data['sender'] not in users:
            raise serializers.ValidationError('User does not exist')
        
        # Check content length
        content = validated_data['content']
        if len(content) < 10:
            raise serializers.ValidationError("content must be > 10 characters")
        
        # Create the Message instance without the read_by field
        message = Message.objects.create(**validated_data)
        
        # Set the read_by ManyToMany field
        message.read_by.set(read_by_users)
        
        return message
    """
    Create and return a new `Snippet` instance, given the validated data.
    """
    
class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'

    def validate_participants(self, participants):
        """
        Validate that all participants exist in the database.
        """
        users = User.objects.all()
        for participant in participants:
            if participant not in users:
                raise serializers.ValidationError(f"User {participant} does not exist.")
        return participants

    def create(self, validated_data):
        participants = validated_data.get('participants')
        chat = Chat.objects.create()
        chat.participants.set(participants)  # Add participants to the chat

        # Create the message (assuming there's at least one message)
        messages_data = validated_data.get('messages', [])
        if messages_data:
            message_data = messages_data[0]
            message = Message.objects.create(
                chat=chat,
                sender=message_data['sender'],
                content=message_data['content']
            )
            message.read_by.set(message_data.get('read_by', []))  # Add users who read the message

        return chat

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'

  
    

#adding functional or object level validators 


"""
from your_app.models import Chat, Message, User

# Assuming you have a user instance
user = User.objects.get(id=user_id)

# First, create and save a Chat object
chat = Chat()
chat.save()

# Add participants to the chat
chat.participants.add(user)
# If there are more participants, add them in a similar manner

# Now, create a Message object and link it to the previously created Chat
message = Message(chat=chat, sender=user, content="Hello, World!")
message.save()

# If there are users who have read the message, add them
message.read_by.add(user)
# Add more users who read the message in a similar manner


"""