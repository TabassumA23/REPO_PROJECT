<template>
  <div class="reservations-container">
    <h1>Your Reservations</h1>

    <ul v-if="reservations.length">
      <li v-for="reservation in reservations" :key="reservation.id">
        <strong>{{ reservation.restaurant.name }}</strong> - {{ formatDate(reservation.reservation_time) }}
        <button @click="cancelReservation(reservation.id)">Cancel</button>
      </li>
    </ul>
    <p v-else>You have no reservations.</p>

    <h2>Book a Reservation</h2>
    <form @submit.prevent="bookReservation">
      <label>Restaurant:
        <select v-model="selectedRestaurant">
          <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.id">
            {{ restaurant.name }}
          </option>
        </select>
      </label>
      <label>Reservation Time:
        <input type="datetime-local" v-model="reservationTime" required />
      </label>
      <label>Number of People:
        <input type="number" v-model="peopleCount" min="1" required />
      </label>
      <button type="submit">Book Now</button>
    </form>
  </div>
  <router-link to="/profile">
    <button class="back-btn">Back to Profile</button>
    </router-link>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import axios from "axios";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();
const userId = computed(() => userStore.user?.id);

const reservations = ref([]);
const restaurants = ref([]);
const selectedRestaurant = ref("");
const reservationTime = ref("");
const peopleCount = ref(1);

const headers = {
  Authorization: `Bearer ${localStorage.getItem("token")}`,
  "Content-Type": "application/json",
};

// Fetch Reservations
const fetchReservations = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/reservations/", { headers });
    reservations.value = res.data;
  } catch (error) {
    console.error("Error fetching reservations:", error);
  }
};

// Fetch Restaurants
const fetchRestaurants = async () => {
  try {
    const restRes = await axios.get("http://127.0.0.1:8000/api/restaurants/", { headers });
    restaurants.value = restRes.data;
  } catch (error) {
    console.error("Error fetching restaurants:", error);
  }
};

// Watch for userId and Fetch Data
watch(userId, (newId) => {
  if (newId) {
    fetchReservations();
    fetchRestaurants();
  }
}, { immediate: true });

// Book a Reservation
const bookReservation = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/api/reservations/", {
      user_id: userId.value,
      restaurant_id: selectedRestaurant.value,
      reservation_time: reservationTime.value,
      number_of_people: peopleCount.value,
    }, { headers });

    fetchReservations(); // Refresh after booking
  } catch (error) {
    console.error("Error booking reservation:", error);
  }
};

// Cancel a Reservation
const cancelReservation = async (reservationId: number) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/reservations/${reservationId}/`, { headers });
    reservations.value = reservations.value.filter(res => res.id !== reservationId);
  } catch (error) {
    console.error("Error canceling reservation:", error);
  }
};

// Format Date
const formatDate = (dateStr: string) => new Date(dateStr).toLocaleString();
</script>

<style scoped>
.reservations-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

button {
  margin: 5px;
  padding: 8px;
  background-color: red;
  border: none;
  color: white;
  cursor: pointer;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

</style>
