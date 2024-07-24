from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    #full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # FIELD VALIDATION syntax validate_<field name>
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password length should not be less than 8")
        return value

    # Uncomment and use this for object-level validation
    # def validate(self, data):
    #     if len(data['password']) < 6:
    #         raise serializers.ValidationError('Password must be at least 6 characters long')
    #     return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user