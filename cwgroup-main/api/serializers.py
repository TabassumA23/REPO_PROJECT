from rest_framework import serializers
from .models import Restaurant, Review, Reservation, Wishlist, RestaurantSiteUser, Cuisine

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantSiteUser
        fields = ['id', 'username', 'email', 'fav_cuisines', 'dietary_restrictions', 'saved_restaurants']

# ✅ Restaurant Serializer
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

# ✅ Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'restaurant', 'rating', 'comment', 'created_at']

# ✅ Reservation Serializer
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'restaurant', 'reservation_time', 'number_of_people', 'status']

# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    restaurants = RestaurantSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'name', 'restaurants']

# Cuisine Serializer
class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['name'] 
