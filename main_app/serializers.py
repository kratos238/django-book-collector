from rest_framework import serializers
from .models import Book, ReadingSession, Tag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user


class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model = Tag
      fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

class ReadingSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ReadingSession
    fields = '__all__'
    read_only_fields = ('Book',)


