<template>
  <div class="search-container">
    <h1>Find Restaurants</h1>
    <input v-model="searchQuery" placeholder="Search restaurants..." />
    
    <!-- Filters -->
    <div class="filters">
      <label>Cuisine:
        <select v-model="selectedCuisine">
          <option value="">All</option>
          <option v-for="cuisine in cuisines" :key="cuisine.id" :value="cuisine.id">
            {{ cuisine.name }}
          </option>
        </select>
      </label>

      <label>Price:
        <select v-model="selectedPrice">
          <option value="">Any</option>
          <option value="$">$ (Cheap)</option>
          <option value="$$">$$ (Moderate)</option>
          <option value="$$$">$$$ (Expensive)</option>
        </select>
      </label>
    </div>

    <!-- Restaurant List -->
    <ul>
      <li v-for="restaurant in filteredRestaurants" :key="restaurant.id">
        <h3>{{ restaurant.name }}</h3>
        <p>{{ restaurant.address }}</p>
        <p>Price: {{ restaurant.price_range }}</p>
        <button @click="saveRestaurant(restaurant.id)">Save</button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const searchQuery = ref("");
const selectedCuisine = ref("");
const selectedPrice = ref("");

const restaurants = ref([]);
const cuisines = ref([]);

onMounted(async () => {
  const res = await axios.get("http://127.0.0.1:8000/restaurants/");
  restaurants.value = res.data.restaurants;

  const cuisineRes = await axios.get("http://127.0.0.1:8000/cuisines/");
  cuisines.value = cuisineRes.data.cuisines;
});

const filteredRestaurants = computed(() =>
  restaurants.value.filter((r) =>
    (searchQuery.value === "" || r.name.toLowerCase().includes(searchQuery.value.toLowerCase())) &&
    (selectedCuisine.value === "" || r.cuisine.id === selectedCuisine.value) &&
    (selectedPrice.value === "" || r.price_range === selectedPrice.value)
  )
);

const saveRestaurant = async (restaurantId: number) => {
  await axios.post(`http://localhost:8000/user/save-restaurant/`, { restaurant_id: restaurantId });
};
</script>

<style scoped>
.search-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
.filters {
  display: flex;
  justify-content: space-around;
}
button {
  padding: 8px;
  margin: 5px;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
