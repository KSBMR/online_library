from django.db import models
import os
from django.contrib.auth.models import User

# Create your models here.

def books_directory_path(instance, filename):
    return os.path.join('books', instance.catagory, filename)

class Add_Book(models.Model):
    title= models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    catagory = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to=books_directory_path, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    book = models.ForeignKey(Add_Book, on_delete=models.CASCADE, related_name='reviews')
    review= models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}-{self.book.title}-{self.book.id}-{self.rating}-{self.review}"
    