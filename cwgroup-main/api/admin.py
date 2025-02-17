from django.contrib import admin
from .models import (
    RestaurantSiteUser, Cuisine, DietaryRestriction, Restaurant,
    Review, Reservation, Wishlist, Recommendation, PageView
)

# Custom UserAdmin
@admin.register(RestaurantSiteUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'custom_fav_cuisines', 'custom_dietary_restrictions')

    def custom_fav_cuisines(self, obj):
        return ", ".join([cuisine.name for cuisine in obj.fav_cuisines.all()])
    custom_fav_cuisines.short_description = 'Favorite Cuisines'

    def custom_dietary_restrictions(self, obj):
        return ", ".join([restriction.name for restriction in obj.dietary_restrictions.all()])
    custom_dietary_restrictions.short_description = 'Dietary Restrictions'

# Cuisine Admin
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)

# DietaryRestriction Admin
@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Restaurant Admin
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'cuisine', 'price_range', 'custom_dietary_options')

    def custom_dietary_options(self, obj):
        return ", ".join([restriction.name for restriction in obj.dietary_options.all()])
    custom_dietary_options.short_description = 'Dietary Options'

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'comment', 'created_at')

# Reservation Admin
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'reservation_time', 'number_of_people', 'status')

# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'custom_restaurants')

    def custom_restaurants(self, obj):
        return ", ".join([restaurant.name for restaurant in obj.restaurants.all()])
    custom_restaurants.short_description = 'Restaurants'

# Recommendation Admin
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'reason')

# PageView Admin
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('count',)