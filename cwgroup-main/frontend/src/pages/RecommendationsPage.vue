<template>
  <div class="recommendations-container">
    <h1>Recommended for You</h1>

    <ul v-if="recommendations.length">
      <li v-for="restaurant in recommendations" :key="restaurant.id">
        {{ restaurant.name }} - {{ restaurant.address }}
      </li>
    </ul>
    <p v-else>No recommendations available.</p>

    <router-link to="/profile">
      <button class="back-btn">Back to Profile</button>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const recommendations = ref([]);

onMounted(async () => {
  const res = await axios.get("http://127.0.0.1:8000/recommendations/");
  recommendations.value = res.data.recommendations;
});
</script>

<style scoped>
.recommendations-container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
</style>
