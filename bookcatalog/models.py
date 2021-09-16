from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import OneToOneField
from django.db.models import Avg

# Create your models here.


class Reader(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    cover_page_url = models.URLField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

        if avg_rating is not None:
            return round(avg_rating, 2)
        else:
            return 0


class Review(models.Model):
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING)
    comments = models.TextField(max_length=4000)
    created_by = models.ForeignKey(Reader, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_by} - {self.book}'


class ReadingList(models.Model):
    list_name = models.CharField(max_length=100, default='Books')
    created_by = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.created_by} - {self.list_name}'


class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reading_list} - {self.book}'


class FriendsList(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader}'s Friends"


class Friend(models.Model):
    friends_list = models.ForeignKey(FriendsList, on_delete=models.CASCADE)
    friend = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.friends_list} - {self.friend}'