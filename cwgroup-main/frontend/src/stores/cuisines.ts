import { defineStore } from "pinia"; 
import axios from "axios";
import { useAuthStore } from "./auth";

export const useCuisinesStore = defineStore("cuisines", {
  state: () => ({
    cuisines: [],
  }),

  actions: {
    async fetchCuisines() {
      const authStore = useAuthStore();
      if (!authStore.accessToken) {
        console.error("User not authenticated");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/cuisines/", {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        });

        this.cuisines = response.data; // ✅ Store cuisines
      } catch (error) {
        console.error("Error fetching cuisines:", error.response?.data || error);
      }
    },
  },
});
