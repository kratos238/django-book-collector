from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics
from .models import Book, ReadingSession, Tag
from .serializers import BookSerializer, ReadingSessionSerializer, TagSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the book-collector api home route!'}
    
    return Response(content)

class BookList(generics.ListCreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  lookup_field = 'id'

class ReadingSessionCreate(generics.ListCreateAPIView):
  serializer_class = ReadingSessionSerializer

  def get_queryset(self):
    book_id = self.kwargs['book_id']
    return ReadingSession.objects.filter(book_id=book_id)

  def perform_create(self, serializer):
    book_id = self.kwargs['book_id']
    book = Book.objects.get(id=book_id)
    serializer.save(book=book)

class ReadingSessionDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ReadingSessionSerializer
  lookup_field = 'id'

  def get_queryset(self):
    book_id = self.kwargs['book_id']
    return ReadingSession.objects.filter(book_id=book_id)
  

class TagList(generics.ListCreateAPIView):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'id'