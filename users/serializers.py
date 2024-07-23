


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    #full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
        def validate(self,data):
            if len(data['password'])<6:
                raise serializers.ValidationError('Password must be at least 6 characters long')

        def create(self,validated_data):
            
            
            
            
            user = User.objects.create_user(**validated_data)
            
            
            
            return user
        


"""

 def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
"""
   