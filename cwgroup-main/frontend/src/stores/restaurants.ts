import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./auth";

export const useRestaurantsStore = defineStore("restaurants", {
  state: () => ({
    restaurants: [],
  }),

  actions: {
    async fetchRestaurants() {
      const authStore = useAuthStore();
      if (!authStore.accessToken) {
        console.error("User not authenticated");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/restaurants/", {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },  // ✅ Ensure token is sent
        });

        this.restaurants = response.data;
      } catch (error) {
        console.error("Error fetching restaurants:", error.response?.data || error);
      }
    },
  },
});
