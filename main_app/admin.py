from django.contrib import admin
 # import your models here
from .models import Book, ReadingSession, Tag

# Register your models here
admin.site.register(Book)
admin.site.register(ReadingSession)
admin.site.register(Tag)


