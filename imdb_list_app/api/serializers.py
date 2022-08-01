from attr import fields
from rest_framework import serializers
from imdb_list_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"




    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField()
    # description = serializers.CharField()
    # active = serializers.BooleanField()

    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active', instance.active)
    #     instance.save()
    #     return instance
        
