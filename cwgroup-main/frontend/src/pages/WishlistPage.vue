<template>
  <div class="wishlist-container">
    <h1>Your Wishlist</h1>

    <!-- ✅ Profile Information -->
    <div class="profile-section" v-if="user">
      <h2>Profile Information</h2>
      <p>ID: {{ user?.id || "Not Available" }}</p>
      <p>Username: {{ user?.username || "Not Available" }}</p>
      <p>Email: {{ user?.email || "Not Available" }}</p>
      <button @click="logout">Logout</button>
    </div>

    <p v-if="!user">Loading user...</p>

    <!-- ✅ Wishlist Section -->
    <div class="wishlist-section">
      <h2>Saved Restaurants</h2>
      <p v-if="wishlist.length === 0">You have no saved restaurants.</p>

      <ul v-if="wishlist.length">
        <li v-for="restaurant in wishlist" :key="restaurant.id">
          {{ restaurant.name }} - {{ restaurant.address }}
          <button @click="removeFromWishlist(restaurant.id)">Remove</button>
        </li>
      </ul>
    </div>

    <!-- ✅ Back to Profile -->
    <router-link to="/profile">
      <button class="back-btn">Back to Profile</button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useUserStore } from "../stores/user"; // ✅ Import User Store

const userStore = useUserStore();
const user = computed(() => userStore.user);
const wishlist = ref([]);

const fetchUserAndWishlist = async () => {
  try {
    // Fetch user data
    await userStore.fetchUser();
    console.log(useUserStore().user);

    // Debugging: Check user data
    console.log("User Data:", user.value);

    // Get token from localStorage
    const token = localStorage.getItem("token");
    console.log("Stored Token:", token);  // ✅ Debugging step

    if (!token) {
      console.error("No token found, authentication required.");
      alert("Please log in to view your wishlist.");
      return;
    }

    // Fetch wishlist
    const res = await axios.get("http://127.0.0.1:8000/wishlist/", {
      headers: { Authorization: `Bearer ${token}` },  // ✅ Ensure token is passed
    });

    wishlist.value = res.data;
    console.log("Fetched Wishlist Data:", wishlist.value);
  } catch (error) {
    console.error("Error fetching wishlist:", error);
    alert("Failed to fetch wishlist.");
  }
};


// ✅ Ensure fetching happens when the page loads
onMounted(fetchUserAndWishlist);

// ✅ Logout Function
const logout = () => {
  localStorage.removeItem("token");
  alert("You have been logged out.");
  window.location.href = "/login";
};
</script>

<style scoped>
.wishlist-container {
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

.wishlist-section {
  background: #ffffff;
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

.back-btn {
  margin: 5px;
  padding: 10px;
  background-color: #28a745;
  border: none;
  color: white;
  cursor: pointer;
}
</style>
