<template>
  <div class="reviews-container">
    <h1>Submit a Review</h1>

    <form @submit.prevent="submitReview">
      <label>Restaurant:
        <select v-model="selectedRestaurant">
          <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.id">
            {{ restaurant.name }}
          </option>
        </select>
      </label>
      <label>Rating:
        <input type="number" v-model="selectedRating" min="1" max="5" required />
      </label>
      <label>Review:
        <textarea v-model="reviewText" required></textarea>
      </label>
      <button type="submit">Submit</button>
    </form>

    <router-link to="/profile">
      <button class="back-btn">Back to Profile</button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useUserStore } from "../stores/user"; 

const userStore = useUserStore();
const user = computed(() => userStore.user); // Fix: No need for `[0]`
const userId = computed(() => user.value?.id); 

const selectedRestaurant = ref("");
const selectedRating = ref(5); 
const reviewText = ref("");
const restaurants = ref([]);

const fetchRestaurants = async () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("Authentication required.");
      alert("You must be logged in to view restaurants.");
      return;
    }

    const response = await axios.get("http://127.0.0.1:8000/restaurants/", {
      headers: {
        Authorization: `Bearer ${token}`, // Add Authorization header
      },
    });

    console.log("Fetched Restaurants:", response.data);
    restaurants.value = response.data; 
  } catch (error) {
    console.error("Error fetching restaurants:", error);
    alert("Failed to fetch restaurants. Check your login status.");
  }
};


// Fetch user and restaurants when page loads
onMounted(async () => {
  const token = localStorage.getItem("token"); 
  if (!token) {
    alert("You must be logged in to submit a review!");
    console.error("No token found, authentication required.");
    return;
  }

  await userStore.fetchUser(); // Ensure user data is fetched
  fetchRestaurants();  // Fetch restaurants only if logged in
});
const submitReview = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("You must be logged in to submit a review!");
    console.error("No token found, authentication required.");
    return;
  }

  if (!userId.value) {
    console.error("User ID is undefined! Cannot submit review.");
    return;
  }

  try {
    await axios.post(
      "http://127.0.0.1:8000/review/",
      {
        user_id: userId.value,
        restaurant_id: selectedRestaurant.value,
        rating: selectedRating.value,
        review_text: reviewText.value,
      },
      {
        headers: { 
          Authorization: `Bearer ${token}` // Ensure token is included
        },
      }
    );
    alert("Review submitted successfully!");
  } catch (error) {
    console.error("Error submitting review:", error);
    alert("Failed to submit review. Please try again.");
  }
};

</script>

<style scoped>
.reviews-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
</style>







<template>
  <div class="reviews-container">
    <h1>Submit a Review</h1>

    <form @submit.prevent="submitReview">
      <label>Restaurant:
        <select v-model="selectedRestaurant" required>
          <option disabled value="">Select a restaurant</option>
          <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.id">
            {{ restaurant.name }}
          </option>
        </select>
      </label>

      <label>Rating:
        <input type="number" v-model="selectedRating" min="1" max="5" required />
      </label>

      <label>Review:
        <textarea v-model="reviewText" required></textarea>
      </label>

      <button type="submit">Submit</button>
    </form>

    <router-link to="/profile">
      <button class="back-btn">Back to Profile</button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useUserStore } from "../stores/user";  

const userStore = useUserStore();
const user = computed(() => userStore.user?.[0]);
const userId = computed(() => user?.value?.id);

const selectedRestaurant = ref("");
const selectedRating = ref(5);
const reviewText = ref("");
const restaurants = ref([]);
const isLoading = ref(true);

const fetchRestaurants = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/restaurants/");
    console.log("✅ Fetched Restaurants:", response.data);
    restaurants.value = response.data;
  } catch (error) {
    console.error("❌ Error fetching restaurants:", error);
    alert("Failed to fetch restaurants.");
  }
};





onMounted(async () => {
  await userStore.fetchUser();  // ✅ Ensure user is fetched
  if (!localStorage.getItem("token")) {
    alert("You are not logged in! Redirecting to login.");
    router.push("/login");
    return;
  }
  await fetchRestaurants();
});

const submitReview = async () => {
  if (!userId.value) {
    alert("User ID is missing. Please log in again.");
    console.error("User ID is undefined! Cannot submit review.");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in to submit a review!");
      return;
    }

    await axios.post(
      "http://127.0.0.1:8000/review/",
      {
        user_id: userId.value,
        restaurant_id: selectedRestaurant.value,
        rating: selectedRating.value,
        review_text: reviewText.value,
      },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    alert("Review submitted successfully!");
  } catch (error) {
    console.error("Error submitting review:", error);
    alert("Failed to submit review. Please try again.");
  }
};
</script>

<style scoped>
.reviews-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

button {
  margin-top: 10px;
  padding: 8px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
