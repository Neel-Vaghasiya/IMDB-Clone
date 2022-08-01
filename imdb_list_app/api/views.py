
from .serializers import StreamPlatformSerializer, WatchListSerializer, ReviewSerializer
from imdb_list_app.models import Review, WatchList, StreamPlatform
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .permissions import ReviewUserOrReadOnly, IsAdminOrReadOnly
from .throttling import ReviewCreateThrottle, ReviewListThrottle

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
     
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        user = self.request.user
        review = Review.objects.filter(watchlist=watchlist, review_user = user)
        if(review.exists()):
            raise ValidationError("You have already reviewed this movie")

        if watchlist.total_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.total_rating+=1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user = user)

class UserReviews(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username__icontains = username)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [AnonRateThrottle, ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewUserOrReadOnly]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

class Strem_platformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class Stream_detailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            streamlist = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error":"Platform not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(streamlist)
        return Response(serializer.data)

    def put(self, request, pk):
        streamlist = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(instance=streamlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        streamlist = StreamPlatform.objects.get(pk = pk)
        streamlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class watch_listAV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)    

class watch_detailAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
            return Response({"error":"Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(instance=watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # Create your views here.
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:
#             return Response({"error":"Movie not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(instance=movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)