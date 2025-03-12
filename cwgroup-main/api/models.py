from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

# Custom User Model
class RestaurantSiteUser(AbstractUser):
    fav_cuisines = models.ManyToManyField("Cuisine", blank=True)
    dietary_restrictions = models.ManyToManyField("DietaryRestriction", blank=True)
    disliked_restaurants = models.ManyToManyField("Restaurant", blank=True, related_name="disliked_by")
    saved_restaurants = models.ManyToManyField("Restaurant", blank=True, related_name="saved_by")
    groups = models.ManyToManyField(Group, related_name="restaurant_site_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="restaurant_site_users_permissions", blank=True)

    def __str__(self):
        return self.username

# Cuisine Model
class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Dietary Restrictions Model
class DietaryRestriction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    dietary_options = models.ManyToManyField(DietaryRestriction, blank=True)
    price_range = models.CharField(max_length=50, choices=[("$", "Cheap"), ("$$", "Moderate"), ("$$$", "Expensive")])
    opening_hours = models.JSONField()  # Example: {"Monday": "9AM-10PM"}
    website = models.URLField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    available_seats = models.IntegerField(default=0)  # ✅ Make sure this field exists!

    def __str__(self):
        return self.name


# Reservation Model
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
    
    def save(self, *args, **kwargs):
        if self.restaurant.available_seats >= self.number_of_people:
            self.restaurant.available_seats -= self.number_of_people
            self.restaurant.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough seats available")
    
    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} on {self.reservation_time}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating}/5)"

# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    restaurants = models.ManyToManyField(Restaurant, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.name}"

# Recommendation Model
class Recommendation(models.Model):
    user = models.ForeignKey(RestaurantSiteUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.restaurant.name}"
