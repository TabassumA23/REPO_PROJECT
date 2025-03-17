import { defineStore } from "pinia";

export const useReservationsStore = defineStore("reservations", {
  state: () => ({
    reservations: [],
  }),
  actions: {
    async fetchReservations() {
        try {
          const token = localStorage.getItem("token");
          if (!token) {
            console.error("No token found, authentication required.");
            return;
          }
      
          const response = await fetch("http://localhost:8000/reservations/", {
            headers: { Authorization: `Bearer ${token}` }, // ✅ Include token
          });
      
          if (!response.ok) {
            throw new Error(`HTTP Error! Status: ${response.status}`);
          }
      
          const data = await response.json();
          this.reservations = data;  // ✅ Store response
        } catch (error) {
          console.error("Error fetching reservations:", error);
        }
      },      
      
  },
});
