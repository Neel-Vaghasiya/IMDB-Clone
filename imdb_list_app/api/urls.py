# from .views import movie_details, movie_list
from .views import watch_listAV, watch_detailAV, Strem_platformAV, Stream_detailAV, ReviewList, ReviewDetail, ReviewCreate, UserReviews
from django.urls import path

urlpatterns = [
    path('list/', watch_listAV.as_view(), name='movie-list'),
    path('list/<str:pk>/', watch_detailAV.as_view(), name='movie-detail'),

    path('platforms/', Strem_platformAV.as_view(), name='platform-list'),
    path('platforms/<str:pk>/', Stream_detailAV.as_view(), name='stream-detail'),

    path('list/<str:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('list/<str:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('list/reviews/<str:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReviews.as_view(), name='user-reviews'),
    # path('list/review/<str:username>', UserReviews.as_view(), name='user-reviews'),
]