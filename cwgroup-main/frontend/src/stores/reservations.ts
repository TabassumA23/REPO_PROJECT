import { defineStore } from "pinia"; 
import axios from "axios";
import { useAuthStore } from "./auth";

export const useReservationsStore = defineStore("reservations", {
  state: () => ({
    reservations: [],
  }),

  actions: {
    async fetchReservations() {
      const authStore = useAuthStore();
      if (!authStore.accessToken) {
        console.error("User not authenticated");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/reservations/", {
          headers: { Authorization: `Bearer ${authStore.accessToken}` },
        });

        this.reservations = response.data; // ✅ Store reservations
      } catch (error) {
        console.error("Error fetching reservations:", error.response?.data || error);
      }
    },
  },
});
