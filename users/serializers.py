


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    #full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','username','email','password']

        def validate(self,data):
            if len(data['password'])<6:
                raise serializers.ValidationError('Password must be at least 6 characters long')

        def create(self,validated_data):
            
            """
            print(validated_data['password'])
            if len(validated_data['password'])<6:
                raise serializers.ValidationError('Password must be at least 6 characters long')
            """
            
            
            return User.objects.create_user(**validated_data)
"""

 def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
"""
   