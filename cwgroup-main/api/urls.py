from django.urls import path
from .views import (
    main_spa, signup_api, login_api, logout_api,
    restaurants_api, restaurant_api,
    submit_review, restaurant_reviews,
    make_reservation,
    wishlist_api,
    recommendations_api,
    restaurant_site_users_api,  
    restaurant_site_user_api, 
    RestaurantListView,
    get_cuisines, update_favorite_cuisines,
    reservations_api,
    
)
from django.contrib import admin

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Serve Main Vue.js SPA (Frontend)
    path('', main_spa, name='main_spa'),

    # 🔹 Authentication Endpoints
    path('signup/', signup_api, name='signup_api'),
    path('login/', login_api, name='login_api'),
    path('logout/', logout_api, name='logout_api'),


    path('users/', restaurant_site_users_api, name='restaurant_site_users_api'),  # ✅ For listing users
    path('users/<int:user_id>/', restaurant_site_user_api, name='restaurant_site_user_api'),  # ✅ For fetching a specific user

    # 🔹 Restaurant Endpoints
    path("restaurants/", RestaurantListView.as_view(), name="restaurants_api"),  # Get all or filter restaurants
    path('restaurant/<int:restaurant_id>/', restaurant_api, name='restaurant_api'),  # Get/update/delete restaurant

    # 🔹 Review Endpoints
    path('review/', submit_review, name='submit_review'),  # Submit a review
    path('reviews/<int:restaurant_id>/', restaurant_reviews, name='restaurant_reviews'),  # Get reviews for a restaurant

    # 🔹 Reservation Endpoints
    path('reservation/', make_reservation, name='make_reservation'),  # Make a reservation
    #path("reservations/", reservations_api, name="reservations_api"),
    #path("reservation/<int:reservation_id>/", reservation_api, name="reservation_api"),
    
    # 🔹 Wishlist Endpoints
    path('wishlist/', wishlist_api, name='wishlist_api'),  # Create & retrieve wishlist

    # 🔹 Recommendation Endpoints
    path('recommendations/', recommendations_api, name='recommendations_api'),  # Get personalized recommendations

    path('cuisines/', get_cuisines, name='get_cuisines'),
    path('update_favorite_cuisines/', update_favorite_cuisines, name='update_favorite_cuisines'),

    path("reservations/", reservations_api, name="reservations_api"),
]
