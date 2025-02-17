from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    
# RestaurantSiteUser model 
class RestaurantSiteUser(AbstractUser):
    fav_cuisines = models.ManyToManyField("Cuisine", blank=True)
    dietary_restrictions = models.ManyToManyField("DietaryRestriction", blank=True)
    disliked_restaurants = models.ManyToManyField("Restaurant", blank=True, related_name="disliked_by")
    saved_restaurants = models.ManyToManyField("Restaurant", blank=True, related_name="saved_by")
    groups = models.ManyToManyField(
        Group,
        # Custom related name
        related_name="restaurant_site_users",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        # Custom related name
        related_name="restaurant_site_users_permissions",  
        blank=True
    )

    def __str__(self):
        return self.username

# Cuisine model
class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
# Dietary Restrictions model
class DietaryRestriction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Restaurant model
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    dietary_options = models.ManyToManyField(DietaryRestriction, blank=True)
    price_range = models.CharField(max_length=50, choices=[("$", "Cheap"), ("$$", "Moderate"), ("$$$", "Expensive")])
    opening_hours = models.JSONField()  # Example: {"Monday": "9AM-10PM", "Tuesday": "9AM-10PM"}
    website = models.URLField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name

# Review model
class Review(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    #images = models.ImageField(upload_to="review_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating}/5)"

# Reservation model
class Reservation(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} on {self.reservation_time}"

# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    restaurants = models.ManyToManyField(Restaurant, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.name}"

# Recommendation model
class Recommendation(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)  # Example: "Based on your likes", "Highly rated near you"

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.restaurant.name}"

