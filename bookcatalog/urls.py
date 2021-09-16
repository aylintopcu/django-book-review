from django.urls import path
from bookcatalog.views import BookListView, BookDetailView, ProfileView, ReadingListView, AddToListView, \
     CreateReadingListView, ProfilesListView, SearchResultsView, RatingFilterView, FriendsListView, AddFriendView, EditReviewView

app_name = 'bookcatalog'
urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('filter/', RatingFilterView.as_view(), name='rating_filter'),
    path('genres/<int:genre>/', BookListView.as_view(), name='genre_book_list'),
    path('<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:book_id>/edit_review/', EditReviewView.as_view(), name='edit_review'),
    path('<int:book_id>/add/', AddToListView.as_view(), name='add_to_list'),
    path('profiles/', ProfilesListView.as_view(), name='profiles_list'),
    path('profiles/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profiles/<str:username>/<int:reading_list_id>/', ReadingListView.as_view(), name='reading_list'),
    path('profiles/<str:username>/create_reading_list/', CreateReadingListView.as_view(), name='create_reading_list'),
    path('profiles/<str:username>/friends_list/', FriendsListView.as_view(), name='friends_list'),
    path('profiles/<str:username>/friend/', AddFriendView.as_view(), name='friend'),
]
