from django.urls import path
from .views import Home, BookList, BookDetail, ReadingSessionCreate, ReadingSessionDetail, TagList, TagDetail, AddTagToBook, RemoveTagFromBook

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetail.as_view(), name='book-detail'),
    path('books/<int:book_id>/readingsessions/', ReadingSessionCreate.as_view(), name='reading-session-create'),
	path('books/<int:book_id>/readingsessions/<int:id>/', ReadingSessionDetail.as_view(), name='reading-session-detail'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('tags/<int:id>/',TagDetail.as_view(), name='tag-detail'),
    path('books/<int:book_id>/add_tag/<int:tag_id>/', AddTagToBook.as_view(), name='add-tag-to-book'),
    path('books/<int:book_id>/remove_tag/<int:tag_id>/', RemoveTagFromBook.as_view(), name='remove-tag-from-book'),
]
