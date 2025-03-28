import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./auth"; 

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
  }),

  actions: {
    async fetchUser() {
      const authStore = useAuthStore();
      if (!authStore.accessToken) {
        console.error("User not authenticated, cannot fetch profile");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/users/me/", {
          headers: { Authorization: `Bearer ${authStore.accessToken}` }, 
        });

        this.user = response.data;  
        console.log("Fetched user:", this.user);
      } catch (error) {
        if (error.response?.status === 401) {
          console.warn("Access token expired, refreshing...");
          await authStore.refreshAccessToken(); 
          return this.fetchUser();  
        }

        console.error("Error fetching user:", error.response?.data || error);
      }
    },
    async saveFavoriteCuisines(cuisineIds: number[]) {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in first.");
        return;
      }

      try {
        await axios.post(
          "http://127.0.0.1:8000/update_favorite_cuisines/",
          { cuisine_ids: cuisineIds },
          {
            headers: {
              'Authorization': `Bearer ${VueCookies.get('access_token')}`,
              'Content-Type': 'application/json',
              'X-CSRFToken': VueCookies.get('csrftoken'),
            },
          }
        );

        alert("Preferences saved!");
        await this.fetchUser(); 
      } catch (err) {
        console.error("Failed to save preferences", err);
        alert("Failed to save preferences.");
      }
    },
  },
});
