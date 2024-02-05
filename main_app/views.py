from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

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
