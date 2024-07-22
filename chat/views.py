from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny  # Import AllowAny
from rest_framework.decorators import action  # Import action decorator
from .serializers import ChatSerializer,    MessageSerializer, GroupSerializer
from .models import Chat,Message,ChatGroup
# Create your views here.

def create_room(request):
    if request.method == 'POST':
        global username
        username=request.POST['username']
        global room
        room= request.POST['room']
        try:
            get_Room=ChatGroup.objects.get(group_name=room)
              # Add your code here
        except ChatGroup.DoesNotExist:

            group=ChatGroup()
            group.group_name=room

            #group=ChatGroup(group_name=room).objects.select_related('users').first()
            #group.participant.username=username
            group.save()
            return redirect('room',room_name=room,username=username)
        
    
    return render(request, 'index.html')


def message_view(request,room_name,username):
    """
    group__group_name=room_name: This condition specifies that you want to filter Message objects 
    where the related ChatGroup's group_name attribute equals room_name. 
    The double underscore (__) is used to access related fields.
    
    """
    messages=Message.objects.filter(group__group_name=room_name)
    #chat_group=ChatGroup.objects.get(group_name=room_name)
    #messages=Message.objects.filter(group=chat_group)
    context={
        'message':messages,
        'username':username,
        'chat_group':room_name
    }
    return render(request, '_message.html',context)


class ChatViewset(ModelViewSet):

    serializer_class=ChatSerializer
    permission_classes=[AllowAny]
    queryset=Chat.objects.all()

    def list(self,request,pk=None):
        queryset = Chat.objects.all()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['POST'],detail=False)
    def create_chat(self,request):
        serializer = ChatSerializer(data=request.data)
        if Chat.objects.exists()==False:
             chat=Chat()
             chat.save()
           
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self,request,pk=None):
        queryset = Chat.objects.all()
        chat = get_object_or_404(queryset, pk=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def update(self,request,pk=None):
        #chat = Chat.objects.get(pk=pk)
        chat=Chat.objects.filter(request.user)
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def destroy(self,request,pk=None):
        chat = Chat.objects.get(pk=pk)
        chat.delete()
        return Response(status=204)
    
    @action(methods=['get'],detail=True)
    def chat_messages(self,request,pk):
        # Add your indented block here
        #chat=Chat.objects.get(pk=pk)
        chat= get_object_or_404(Chat, pk=pk)
        messages=chat.messages.all()
        
        serializer=MessageSerializer(messages,many=True)
        return Response(serializer.data)

class MessageViewSet(ModelViewSet):
        serializer_class=MessageSerializer
        queryset=Message.objects.all()
        permission_classes=[AllowAny]

        @action(methods=['PUT'],detail=True)
        def update_content(self, request, pk):
            message = Message.objects.all().filter(id=pk).first()
            serializer = MessageSerializer(message, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    
        @action(methods=['get'],detail=False)
        def get_list(self,request):
            queryset = Message.objects.all()
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)
        
        @action(methods=['delete'],detail=True)
        def delete_message(self,request,pk):
            message=Message.objects.get(pk=pk)
            message.delete()
            return Response(status=204)
        
        @action(methods=['post'], detail=False)
        def create_message(self,request):
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        

       
        
       
    
       

        
        """
 def destroy(self,request,pk=None):
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response(status=204)

        """
    
       


class GroupView(ModelViewSet):
    
    serializer_class=GroupSerializer
    queryset=ChatGroup.objects.all()
    permission_classes=[AllowAny]

    @action(methods=['post'],detail=True)
    def create_group(self,request,pk):
        data=   {"room":room,"username":username}
        serializer=GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    @action(methods=['get'],detail=False)
    def get_groups(self,request):
        queryset=ChatGroup.objects.all()
        serializer=GroupSerializer(queryset,many=True)
        return Response(serializer.data)
        
              

      
