import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import check_password
from .models import (
    RestaurantSiteUser, Cuisine, DietaryRestriction, 
    Restaurant, Review, Reservation, Wishlist, Recommendation
)
from .forms import SignUpForm
from .serializers import (
    RestaurantSerializer, ReviewSerializer, ReservationSerializer, WishlistSerializer, UserSerializer, CuisineSerializer
)
from datetime import datetime


def main_spa(request):
    """Render the main Single Page Application (SPA) for Vue.js frontend."""
    return render(request, 'api/spa/index.html', {})

# Signup API
@csrf_exempt
def signup_api(request):
    """API for user signup"""
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body)
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not username or not email or not password:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if RestaurantSiteUser.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = RestaurantSiteUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

        return JsonResponse({"message": "Signup successful!"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
#login api
@csrf_exempt
def login_api(request):
    """API to authenticate users and return JWT tokens."""
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        # Authenticate user from RestaurantSiteUser
        try:
            user = RestaurantSiteUser.objects.get(username=username)
        except RestaurantSiteUser.DoesNotExist:
            return JsonResponse({"error": "Invalid username or password"}, status=401)

        if not check_password(password, user.password):
            return JsonResponse({"error": "Invalid username or password"}, status=401)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return JsonResponse({
            "message": "Login successful",
            "access": access_token,
            "refresh": str(refresh),  # ✅ Send refresh token as well
            "user_id": user.id
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request format"}, status=400)
    
# Logout API
@api_view(['POST'])
@login_required
def logout_api(request):
    """API for user logout"""
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class RestaurantListView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response({"restaurants": serializer.data})
    
@api_view(["GET"])
@permission_classes([AllowAny])
def restaurants_api(request):
    try:
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=200)
    except Exception as e:
        print("Error fetching restaurants:", str(e))  # Debugging
        return Response({"error": str(e)}, status=500)

# Retrieve, update, or delete a restaurant
@api_view(['GET', 'PUT', 'DELETE'])
def restaurant_api(request, restaurant_id):
    """Retrieve, update, or delete a specific restaurant."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        restaurant.name = data.get("name", restaurant.name)
        restaurant.address = data.get("address", restaurant.address)
        restaurant.save()
        return Response({"message": "Restaurant updated successfully"})

    if request.method == 'DELETE':
        restaurant.delete()
        return Response({"message": "Restaurant deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    serializer = RestaurantSerializer(restaurant)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Submit a restaurant review


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only logged-in users can submit reviews
def submit_review(request):
    """API to submit a review."""
    data = request.data
    user = request.user  # This should be set correctly if JWT is working

    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    restaurant = get_object_or_404(Restaurant, id=data.get("restaurant_id"))

    review = Review.objects.create(
        user=user,
        restaurant=restaurant,
        rating=data["rating"],
        comment=data.get("comment", "")
    )

    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewViewSet(viewsets.ModelViewSet):
    """Handles Review CRUD Operations"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]  # ✅ Fix: JWT Authentication required
    permission_classes = [IsAuthenticated]  # ✅ Ensures only logged-in users can post  

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # ✅ Allows anyone to read reviews
        return [IsAuthenticated()]  # ✅ Requires authentication for creating/editing reviews
    
# 📌 Get all reviews for a restaurant
@api_view(['GET'])
def restaurant_reviews(request, restaurant_id):
    """Retrieve all reviews for a specific restaurant."""
    reviews = Review.objects.filter(restaurant__id=restaurant_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 📌 Make a reservation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_reservation(request):
    """API for making a restaurant reservation."""
    data = request.data
    user = request.user
    restaurant = get_object_or_404(Restaurant, id=data.get("restaurant_id"))
    
    reservation_time = datetime.strptime(data["reservation_time"], "%Y-%m-%d %H:%M:%S")
    number_of_people = data["number_of_people"]

    # Ensure the restaurant has availability
    if restaurant.opening_hours.get(reservation_time.strftime("%A"), "Closed") == "Closed":
        return Response({"error": "Restaurant is closed at this time"}, status=status.HTTP_400_BAD_REQUEST)

    reservation = Reservation.objects.create(
        user=user,
        restaurant=restaurant,
        reservation_time=reservation_time,
        number_of_people=number_of_people
    )

    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 📌 Wishlist API
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])  # Ensure token authentication
@permission_classes([IsAuthenticated])  # Require user login
def wishlist_api(request):
    """Retrieve and manage the user's wishlist restaurants."""
    user = request.user

    # ✅ Handle GET request - Return restaurants in the user's wishlist
    if request.method == 'GET':
        wishlist_items = Wishlist.objects.filter(user=user)

        if not wishlist_items.exists():
            return Response({"wishlist": []}, status=status.HTTP_200_OK)

        # Extract only the restaurant objects
        restaurants = [item.restaurant for item in wishlist_items]
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response({"wishlist": serializer.data}, status=status.HTTP_200_OK)

    # ✅ Handle POST request - Add a restaurant to the wishlist
    elif request.method == 'POST':
        data = request.data
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return Response({"error": "Restaurant ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = Restaurant.objects.filter(id=restaurant_id).first()
        if not restaurant:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the restaurant is already in the user's wishlist
        if Wishlist.objects.filter(user=user, restaurant=restaurant).exists():
            return Response({"message": "Restaurant already in wishlist"}, status=status.HTTP_200_OK)

        # Add restaurant to wishlist
        Wishlist.objects.create(user=user, restaurant=restaurant)

        return Response({"message": "Restaurant added to wishlist"}, status=status.HTTP_201_CREATED)
    
# 📌 Recommendation API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations_api(request):
    """API to generate restaurant recommendations based on user preferences."""
    user = request.user
    fav_cuisines = user.fav_cuisines.all()
    disliked_restaurants = user.disliked_restaurants.all()

    recommended_restaurants = Restaurant.objects.filter(cuisine__in=fav_cuisines).exclude(id__in=disliked_restaurants)
    
    serializer = RestaurantSerializer(recommended_restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def restaurant_site_users_api(request):
    """Retrieve all users"""
    users = list(RestaurantSiteUser.objects.values("id", "username", "email"))
    return JsonResponse({"users": users})

def restaurant_site_user_api(request, user_id):
    """Retrieve a specific user"""
    try:
        user = RestaurantSiteUser.objects.get(id=user_id)
        return JsonResponse({"id": user.id, "username": user.username, "email": user.email})
    except RestaurantSiteUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])  # Publicly accessible
def get_cuisines(request):
    """Retrieve all available cuisines."""
    cuisines = Cuisine.objects.all()
    serializer = CuisineSerializer(cuisines, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requires login
def update_favorite_cuisines(request):
    """Update user's favorite cuisines."""
    user = request.user  # Ensure user is authenticated
    data = request.data
    cuisine_ids = data.get("cuisine_ids", [])  # List of selected cuisine IDs

    if not cuisine_ids:
        return Response({"error": "No cuisines selected"}, status=400)

    selected_cuisines = Cuisine.objects.filter(id__in=cuisine_ids)
    user.fav_cuisines.set(selected_cuisines)  # Update ManyToManyField

    return Response({"message": "Favorite cuisines updated successfully"}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])  # ✅ Ensures only logged-in users can access
def reservations_api(request):
    """Retrieve all reservations for the logged-in user."""
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Returns the currently authenticated user's info."""
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_favorite_cuisines(request):
    user = request.user
    cuisine_ids = request.data.get("cuisine_ids", [])

    # Assuming user has a ManyToMany field: fav_cuisines
    user.fav_cuisines.set(Cuisine.objects.filter(id__in=cuisine_ids))
    user.save()

    return Response({"status": "Cuisines updated successfully"})