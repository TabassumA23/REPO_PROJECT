import { defineStore } from "pinia";

export const useReservationsStore = defineStore("reservations", {
  state: () => ({
    reservations: [],
  }),
  actions: {
    async fetchReservations() {
      try {
        const response = await fetch("http://localhost:8000/reservations/");
        const data = await response.json();
        this.reservations = data.reservations;
      } catch (error) {
        console.error("Error fetching reservations:", error);
      }
    },
  },
});
