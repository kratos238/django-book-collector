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

  # add (override) the retrieve method below
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # Get the list of toys not associated with this cat
    tags_not_associated = Tag.objects.exclude(id__in=instance.tags.all())
    tags_serializer = TagSerializer(tags_not_associated, many=True)

    return Response({
        'book': serializer.data,
        'tags_not_associated': tags_serializer.data
    })

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

class AddTagToBook(APIView):
  def post(self, request, book_id, tag_id):
    book = Book.objects.get(id=book_id)
    tag = Tag.objects.get(id=tag_id)
    book.tags.add(tag)
    return Response({'message': f'Book {tag.name} added to book {book.title}'})


class RemoveTagFromBook(APIView):
  def post(self, request, book_id, tag_id):
    book = Book.objects.get(id=book_id)
    tag = Tag.objects.get(id=tag_id)
    book.tags.remove(tag)
    return Response({'message': f'Book {tag.name} removed from book {book.title}'})