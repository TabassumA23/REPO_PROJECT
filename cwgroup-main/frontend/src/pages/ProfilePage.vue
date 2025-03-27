<template>
  <div class="profile-container">
   <!-- Navigation to other pages -->
    <div class="profile-section">
      <h2>Manage Your Account</h2>
      <router-link to="/reservations">
        <button class="nav-btn">Make Reservations</button>
      </router-link>
      <router-link to="/wishlist">
        <button class="nav-btn">View Wishlist</button>
      </router-link>
      <router-link to="/reviews">
        <button class="nav-btn">Submit a Review</button>
      </router-link>
      <router-link to="/recommendations">
        <button class="nav-btn">Get Recommendations</button>
      </router-link>
    </div>

    <h1>Welcome, {{ userStore.user?.username || "Guest" }}</h1>


    <div class="profile-section">
    <h2>Profile Information</h2>
    <p>ID: {{ userStore.user?.id }}</p>  
    <p>Username: {{ userStore.user?.username }}</p>
    <p>Email: {{ userStore.user?.email }}</p>

    <button @click="logout">Logout</button>
    </div>

    <div>
    <h2>All Restaurants</h2>
    <ul v-if="restaurantsStore.restaurants.length">
      <li v-for="restaurant in restaurantsStore.restaurants" :key="restaurant.id">
        {{ restaurant.name }} - {{ restaurant.address }}
      </li>
    </ul>
    <p v-else>No restaurants available.</p>
    </div>


   
  

   <div class="profile-section">
    <h2>Favorite Cuisines</h2>
    <ul>
      <li v-for="cuisine in user?.fav_cuisines" :key="cuisine.id">
        {{ cuisine.name }}
      </li>
    </ul>
  </div>


   
    <!-- Favorite Cuisines -->
    <div class="favcuisine-section">
    <h2>Select Your Favorite Cuisines</h2>
    <form @submit.prevent="saveFavoriteCuisines">
        <div v-for="cuisine in cuisinesStore.cuisines" :key="cuisine.id">  <!-- ✅ Fix here -->
        <label>
            <input 
            type="checkbox" 
            :value="cuisine.id" 
            v-model="selectedCuisines" 
            />
            {{ cuisine.name }}
        </label>
        </div>
        <button type="submit">Save Preferences</button>
    </form>
    </div>

  
    <!-- Dietary Restrictions -->
    <div class="profile-section">
      <h2>Dietary Restrictions</h2>
      <ul>
        <li v-for="restriction in user?.dietary_restrictions" :key="restriction.id">
          {{ restriction.name }}
        </li>
      </ul>
    </div>

    <!-- Saved Restaurants -->
    <div class="profile-section">
      <h2>Saved Restaurants</h2>
      <ul>
        <li v-for="restaurant in user?.saved_restaurants" :key="restaurant.id">
          {{ restaurant.name }} - {{ restaurant.address }}
          <button @click="removeSavedRestaurant(restaurant.id)">Remove</button>
        </li>
      </ul>
    </div>

    <!-- Reservations -->
    <div class="profile-section">
      <h2>Your Reservations</h2>
      <router-link to="/reservations">
        <button class="reservations-btn">View Reservations</button>
      </router-link>
      <ul>
        <li v-for="reservation in reservations" :key="reservation.id">
          {{ reservation.restaurant.name }} - {{ reservation.reservation_time }}
          <button @click="cancelReservation(reservation.id)">Cancel</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref} from "vue"; 
import { useUserStore } from "../stores/user";  
import { useReservationsStore } from "../stores/reservations"; 
import { useRestaurantsStore } from "../stores/restaurants";
import { useCuisinesStore } from "../stores/cuisines";
import { useAuthStore } from "../stores/auth";


const userStore = useUserStore();
const reservationsStore = useReservationsStore(); 
const restaurantsStore = useRestaurantsStore();
const cuisinesStore = useCuisinesStore();
const authStore = useAuthStore();

const user = computed(() => userStore.user);
const selectedCuisines = ref(null);

const saveFavoriteCuisines = () => {
  userStore.saveFavoriteCuisines(selectedCuisines.value);
};

onMounted(async () => {
  if (!authStore.accessToken) {
    console.error("User is not authenticated");
    return;
  }

  await authStore.fetchUser();
  await restaurantsStore.fetchRestaurants();
  await reservationsStore.fetchReservations();
  await cuisinesStore.fetchCuisines();

  await userStore.fetchUser();
});
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

.profile-section {
  background: #f8f9fa;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}

button {
  padding: 8px;
  margin: 5px;
  background-color: #42b983;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
