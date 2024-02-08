from rest_framework import serializers
from .models import Book, ReadingSession, Tag

class TagSerializer(serializers.ModelSerializer):
   class Meta:
      model = Tag
      fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class ReadingSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ReadingSession
    fields = '__all__'
    read_only_fields = ('Book',)


