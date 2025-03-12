<template>
  <div class="restaurants-container">
    <h1>Restaurant List</h1>
    <ul v-if="restaurants.length">
      <li v-for="restaurant in restaurants" :key="restaurant.id">
        {{ restaurant.name }}
      </li>
    </ul>
    <p v-else>No restaurants available.</p>

    <router-link to="/profile">
      <button class="back-btn">Back to Profile</button>
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const restaurants = ref([]);

const fetchRestaurants = async () => {
  try {
    const token = localStorage.getItem("token"); // Get stored token
    const headers = token ? { Authorization: `Bearer ${token}` } : {}; // Add auth token if exists

    const response = await axios.get("http://127.0.0.1:8000/restaurants/", { headers });
    restaurants.value = response.data;
    console.log("Restaurants fetched:", response.data);
  } catch (error) {
    console.error("Error fetching restaurants:", error);
    alert("Failed to fetch restaurants. Please check your login status.");
  }
};

onMounted(fetchRestaurants);
</script>

<style scoped>
.restaurants-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
</style>
