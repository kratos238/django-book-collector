from django.db import models

MOODS = (
    ('H', 'Happy'),
    ('S', 'Sad'),
    ('R', 'Relaxed'),
    ('E', 'Excited'),
    ('C', 'Curious'),
    ('T', 'Tired'),
)


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    genre= models.CharField(max_length=100)
    summary = models.TextField(max_length=250)
    release = models.IntegerField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
      return self.title
    

class ReadingSession(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_sessions')
    date = models.DateField('Reading Date')
    pages_read = models.IntegerField(default=0)  # The number of pages read during the session
    mood = models.CharField(
        max_length=1,
        choices=MOODS,
        blank=True,  # Keeping it optional
    )  # Optional mood of the reader
    location = models.CharField(max_length=100, blank=True)  # Optional reading location

    def __str__(self):
        return f"{self.book.title} read on {self.date} for {self.pages_read} pages"

    class Meta:
        ordering = ['-date']

