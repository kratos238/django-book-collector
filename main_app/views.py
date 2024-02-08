from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Book, ReadingSession, Tag
from .serializers import BookSerializer, ReadingSessionSerializer, TagSerializer, UserSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the book-collector api home route!'}
    
    return Response(content)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

class BookList(generics.ListCreateAPIView):
  # queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      user = self.request.user
      return Book.objects.filter(user=user)

  def perform_create(self, serializer):
      serializer.save(user=self.request.user)

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
  # queryset = Book.objects.all()
  serializer_class = BookSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Book.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    tags_not_associated = Tag.objects.exclude(id__in=instance.tags.all())
    tags_serializer = TagSerializer(tags_not_associated, many=True)

    return Response({
        'book': serializer.data,
        'tags_not_associated': tags_serializer.data
    })

  def perform_update(self, serializer):
    book = self.get_object()
    if book.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this book."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this book."})
    instance.delete()

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