from django.urls import path
from .views import Home, BookList, BookDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetail.as_view(), name='book-detail'),

]
