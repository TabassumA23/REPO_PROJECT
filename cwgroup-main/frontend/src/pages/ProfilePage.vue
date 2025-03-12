<template>
  <div class="profile-container">
    <h1>Welcome, {{ user?.username || "Guest" }}</h1>

    <div class="profile-section">
    <h2>Profile Information</h2>
    <p>ID: {{ user?.id }}</p>  <!-- Add ID to verify -->
    <p>Username: {{ user?.username }}</p>
    <p>Email: {{ user?.email }}</p>
    <button @click="logout">Logout</button>
    </div>

    <!-- Navigation to other pages -->
    <div class="profile-section">
      <h2>Manage Your Account</h2>
      <router-link to="/reservations">
        <button class="nav-btn">View Reservations</button>
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
  

    <!-- Favorite Cuisines -->
    <div class="profile-section">
      <h2>Favorite Cuisines</h2>
      <ul>
        <li v-for="cuisine in user?.fav_cuisines" :key="cuisine.id">
          {{ cuisine.name }}
        </li>
      </ul>
    </div>

    <div class="profile-container">
    <h1>Welcome, {{ user?.username }}</h1>

    <h2>Select Your Favorite Cuisines</h2>
    <form @submit.prevent="saveFavoriteCuisines">
      <div v-for="cuisine in cuisines" :key="cuisine.id">
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
import { computed, onMounted } from "vue";
import { useUserStore } from "../stores/user";  
import { useReservationsStore } from "../stores/reservations";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const userStore = useUserStore();  
const reservationsStore = useReservationsStore();

const user = computed(() => userStore.user);
const reservations = computed(() => reservationsStore.reservations);

onMounted(async () => {
  await userStore.fetchUser();
  await reservationsStore.fetchReservations();
});


const fetchUser = async () => {
  try {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
      console.error("No user ID found in localStorage");
      return;
    }

    const response = await axios.get(`http://127.0.0.1:8000/users/${userId}/`);
    console.log("Fetched User Data:", response.data);

    userStore.setUser(response.data);  // ✅ Ensure this function exists in the store
  } catch (error) {
    console.error("Error fetching user:", error);
  }
};

// Fetch user when component mounts
onMounted(fetchUser);

const fetchReservations = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/reservations/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.data) throw new Error("No data returned");

    reservationsStore.reservations = response.data;
    console.log("Fetched Reservations:", response.data);
  } catch (error) {
    console.error("Error fetching reservations:", error);
  }
};

const removeSavedRestaurant = async (restaurantId: number) => {
  await axios.delete(`http://localhost:8000/users/${user.value?.id}/remove-saved/${restaurantId}/`);
  await userStore.fetchUser();
};

const cancelReservation = async (reservationId: number) => {
  await axios.delete(`http://localhost:8000/reservation/${reservationId}/`);
  await reservationsStore.fetchReservations();
};

const logout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};
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
