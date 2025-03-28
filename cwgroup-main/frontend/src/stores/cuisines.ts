// src/stores/cuisines.ts
import { defineStore } from 'pinia';
import axios from 'axios';
import { Cuisine } from '../types'; // Make sure this interface exists
import { useAuthStore } from './auth';
import VueCookies from 'vue-cookies';

export const useCuisinesStore = defineStore('cuisines', {
  state: (): { cuisines: Cuisine[] } => ({
    cuisines: [],
  }),

  getters: {
    getCuisineById: (state) => (id: number) => {
      return state.cuisines.find(cuisine => cuisine.id === id);
    },
    getCuisineByName: (state) => (name: string) => {
      return state.cuisines.find(cuisine => cuisine.name === name);
    },
  },

  actions: {
    saveCuisines(cuisines: Cuisine[]) {
      this.cuisines = cuisines;
    },

    addCuisine(cuisine: Cuisine) {
      this.cuisines.push(cuisine);
    },

    removeCuisine(id: number) {
      this.cuisines = this.cuisines.filter(c => c.id !== id);
    },

    async fetchCuisines() {
      const authStore = useAuthStore();
      const token = authStore.accessToken;

      if (!token) {
        console.error("User not authenticated");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/cuisines/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.cuisines = response.data; // ✅ Store the fetched cuisines
      } catch (error: any) {
        console.error("Error fetching cuisines:", error.response?.data || error);
      }
    },
  },
});
