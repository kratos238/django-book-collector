from rest_framework import serializers
from .models import Book, ReadingSession, Tag

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ReadingSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ReadingSession
    fields = '__all__'
    read_only_fields = ('Book',)

class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model = Tag
      fields = '__all__'
