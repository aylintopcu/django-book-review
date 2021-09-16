from django.contrib import admin
from .models import Book, Review, Genre, Reader, ReadingList, ReadingListBook, FriendsList, Friend
# Register your models here.

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Reader)
admin.site.register(ReadingList)
admin.site.register(ReadingListBook)
admin.site.register(FriendsList)
admin.site.register(Friend)
