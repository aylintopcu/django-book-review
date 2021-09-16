from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.views import View
from .models import User, Book, Review, Reader, ReadingList, ReadingListBook, FriendsList, Friend
from .forms import ReviewForm, UpdateProfileForm
from django.db.models import Q
# Create your views here.


class IndexView(View):
    def get(self, request):
        books = Book.objects.order_by('?')[:6]
        science_fiction_books = Book.objects.filter(genre=1).order_by('?')[:6]
        horror_books = Book.objects.filter(genre=2).order_by('?')[:6]
        sports_books = Book.objects.filter(genre=3).order_by('?')[:6]        
        context = {'books': books, 'science_fiction_books': science_fiction_books, 'horror_books': horror_books, 'sports_books': sports_books}
        return render(request, 'bookcatalog/index.html', context)


class BookListView(View):
    def get(self, request, genre=None):
        if genre is not None:
            books = Book.objects.filter(genre=genre)
        else:
            books = Book.objects.all()
        num_books = len(books)
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'num_books': num_books, 'search': '', 'book_rating': ''}
        return render(request, 'bookcatalog/booklist.html', context)


class RatingFilterView(View):
    def get(self, request):
        book_rating = float(request.GET['rating'])
        all_books = Book.objects.all()
            
        books = []
        for book in all_books:
            if book.avg_rating >= book_rating:
                books.append(book)

        num_books = len(books)
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'num_books': num_books, 'search': '', 'book_rating': book_rating}
        return render(request, 'bookcatalog/booklist.html', context)


class SearchResultsView(View):
    def get(self, request):
        search = request.GET['search']
        books = Book.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))
        num_books = len(books)
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'num_books': num_books, 'search': search, 'book_rating': ''}
        return render(request, 'bookcatalog/booklist.html', context)


class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reviews = Review.objects.filter(book=book)
        num_reviews = len(reviews)

        if request.user.is_authenticated:
            reader = Reader.objects.get(user=request.user)
            reading_lists = ReadingList.objects.filter(created_by=reader)
            
            book_in_list = []
            for reading_list in reading_lists:
                reading_list_book = ReadingListBook.objects.filter(book=book, reading_list=reading_list)
                if reading_list_book:
                    book_in_list.append(reading_list.list_name)

            review = Review.objects.filter(created_by=reader, book=book)
            if review:
                reviewed = True
            else:
                reviewed = False

            form = ReviewForm()
            context = {'book': book, 'reader': reader, 'reviews': reviews, 'num_reviews': num_reviews, \
                'reading_lists': reading_lists, 'form': form, 'reviewed': reviewed, 'book_in_list': book_in_list}
            return render(request, 'bookcatalog/bookdetail.html', context)

        else:
            context = {'book': book, 'reviews': reviews, 'num_reviews': num_reviews}
            return render(request, 'bookcatalog/bookdetail.html', context)


    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reviews = Review.objects.filter(book=book)
        form = ReviewForm(request.POST)

        if form.is_valid():
            new_review = form.save(commit=False)
            reader = Reader.objects.get(user=request.user)
            new_review.rating = request.POST['rating3']
            new_review.created_by = reader
            new_review.book = book
            new_review.save()
            book_in_want_to_read_list = ReadingListBook.objects.filter(reading_list__list_name='Want to Read', \
                reading_list__created_by__user=request.user, book=book)
            book_in_currently_reading_list = ReadingListBook.objects.filter(reading_list__list_name='Currently Reading', \
                reading_list__created_by__user=request.user, book=book)
            book_in_read_list = ReadingListBook.objects.filter(reading_list__list_name='Read', \
                reading_list__created_by__user=request.user, book=book)

            if book_in_want_to_read_list: 
                book_in_want_to_read_list.delete()
            
            if book_in_currently_reading_list: 
                book_in_currently_reading_list.delete()

            if not book_in_read_list:
                read_list = get_object_or_404(ReadingList, list_name='Read', created_by=reader)
                read_book = ReadingListBook(book=book, reading_list=read_list)
                read_book.save()
            
            return redirect('bookcatalog:book_detail', book_id=book_id)

        else:
            context = {'book': book, 'reviews': reviews, 'form': form}
            return render(request, 'bookcatalog/bookdetail.html', context)


class ReadingListView(View):
    def get(self, request, reading_list_id, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        reading_list = get_object_or_404(ReadingList, id=reading_list_id)
        books = ReadingListBook.objects.filter(reading_list=reading_list)
        user_friends_list = FriendsList.objects.get(reader__user=request.user)
        user_friend = Friend.objects.filter(friends_list=user_friends_list, friend=reader)
        num_books = len(books)
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'reading_lists': reading_lists, 'reading_list': reading_list, \
            'num_books': num_books, 'reader': reader, 'user_friend': user_friend}
        return render(request, 'bookcatalog/readinglist.html', context)


class ProfilesListView(View):
    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'bookcatalog/profileslist.html', context) 


class ProfileView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        user_friends_list = FriendsList.objects.get(reader__user=request.user)
        user_friend = Friend.objects.filter(friends_list=user_friends_list, friend=reader)
        form = UpdateProfileForm(instance=request.user)
        context = {'reading_lists': reading_lists, 'reader': reader, 'form': form, 'user_friend': user_friend}
        return render(request, 'bookcatalog/profile.html', context)

    def post(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        form = UpdateProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('bookcatalog:profile', username=request.user)

        else:
            context = {'reading_lists': reading_lists, 'reader': reader, 'form': form}
            return render(request, 'bookcatalog/profile.html', context)


class CreateReadingListView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reviews = Review.objects.filter(created_by=reader)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        user_friends_list = FriendsList.objects.get(reader__user=request.user)
        user_friend = Friend.objects.filter(friends_list=user_friends_list, friend=reader)
        context = {'reviews': reviews, 'reading_lists': reading_lists, 'reader': reader, 'user_friend': user_friend}
        return render(request, 'bookcatalog/createreadinglist.html', context)

    def post(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        new_reading_list_name = request.POST['reading_list']
        new_reading_list = ReadingList(created_by=reader, list_name=new_reading_list_name)
        new_reading_list.save()
        reviews = Review.objects.filter(created_by=reader)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        user_friends_list = FriendsList.objects.get(reader__user=request.user)
        user_friend = Friend.objects.filter(friends_list=user_friends_list, friend=reader)
        context = {'reviews': reviews, 'reading_lists': reading_lists, 'reader': reader, 'user_friend': user_friend}
        return render(request, 'bookcatalog/createreadinglist.html', context)


class FriendsListView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reader_friends_list = FriendsList.objects.get(reader=reader)
        reader_friends = Friend.objects.filter(friends_list=reader_friends_list)
        reading_lists = ReadingList.objects.filter(created_by=reader)
        user_friends_list = FriendsList.objects.get(reader__user=request.user)
        user_friend = Friend.objects.filter(friends_list=user_friends_list, friend=reader)
        context = {'reading_lists': reading_lists, 'reader': reader, 'reader_friends': reader_friends, 'user_friend': user_friend}
        return render(request, 'bookcatalog/friendslist.html', context)


class EditReviewView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reader = Reader.objects.get(user=request.user)
        review = get_object_or_404(Review, created_by=reader, book=book)
        form = ReviewForm(instance=review)
        context = {'book': book, review: 'review', 'form': form}
        return render(request, 'bookcatalog/editreview.html', context)
        
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reader = Reader.objects.get(user=request.user)
        review = get_object_or_404(Review, created_by=reader, book=book)
        form = ReviewForm(request.POST, instance=review)
        context = {'book': book, 'review': review, 'form': form}

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.rating = request.POST['rating3']
            new_review.save()
            return redirect('bookcatalog:book_detail', book.pk)
        else:
            form = ReviewForm(instance=review)
            return render(request, 'bookcatalog/editreview.html', context)


class AddToListView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reading_list_id = int(request.POST.get('reading_list_id'))
        reading_list = get_object_or_404(ReadingList, id=reading_list_id)
        book_in_reading_list = ReadingListBook.objects.filter(book=book, reading_list=reading_list)
        book_in_want_to_read_list = ReadingListBook.objects.filter(reading_list__list_name='Want to Read', \
            reading_list__created_by__user=request.user, book=book)
        book_in_currently_reading_list = ReadingListBook.objects.filter(reading_list__list_name='Currently Reading', \
            reading_list__created_by__user=request.user, book=book)
        book_in_read_list = ReadingListBook.objects.filter(reading_list__list_name='Read', \
            reading_list__created_by__user=request.user, book=book)

        if reading_list.list_name != 'Want to Read' and book_in_want_to_read_list: 
            book_in_want_to_read_list.delete()
        
        if reading_list.list_name != 'Currently Reading' and book_in_currently_reading_list: 
            book_in_currently_reading_list.delete()

        if reading_list.list_name != 'Read' and book_in_read_list:
            book_in_read_list.delete()

        if book_in_reading_list:
            book_in_reading_list.delete()
            return JsonResponse({}, status=200)
        else:
            reading_list_book = ReadingListBook(book=book, reading_list=reading_list)
            reading_list_book.save()
            return JsonResponse({}, status=200)


class AddFriendView(View):
    def post(self, request, username):
        user = User.objects.get(username=username)
        reader = Reader.objects.get(user=user)
        reader_friends_list = FriendsList.objects.get(reader=reader)
        
        authenticated_reader = Reader.objects.get(user=request.user)
        authenticated_reader_friends_list = FriendsList.objects.get(reader=authenticated_reader)

        action = request.POST.get('action')

        if action == 'Add Friend':
            add_friend_user = Friend(friends_list=authenticated_reader_friends_list, friend=reader)
            add_friend_user.save()

            add_friend_authenticated_user = Friend(friends_list=reader_friends_list, friend=authenticated_reader)
            add_friend_authenticated_user.save()

            return JsonResponse({}, status=200)

        elif action == 'Remove Friend':
            remove_friend_user = Friend.objects.get(friends_list=authenticated_reader_friends_list, friend=reader)
            remove_friend_user.delete()

            remove_authenticated_user = Friend.objects.get(friends_list=reader_friends_list, friend=authenticated_reader)
            remove_authenticated_user.delete()

            return JsonResponse({}, status=200)

        else:
            return JsonResponse({}, status=400)