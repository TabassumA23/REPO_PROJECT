import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
  }),
  actions: {
    async fetchUser() {
        try {
          const token = localStorage.getItem("token");
          if (!token) return;
  
          const res = await axios.get("http://127.0.0.1:8000/users/", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
  
          this.user = res.data;  // ✅ Store the fetched user
          console.log("User fetched successfully:", this.user);
        } catch (error) {
          console.error("Error fetching user:", error);
        }
      },
    setUser(userData) {  // setUser function
      this.user = userData;
    },
    clearUser() {
      this.user = null;
    },
  },
});
