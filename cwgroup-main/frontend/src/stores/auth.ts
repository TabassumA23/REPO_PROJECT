import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem("accessToken") || null,
    refreshToken: localStorage.getItem("refreshToken") || null,
  }),

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await axios.post("http://127.0.0.1:8000/login/", {
          username,
          password,
        });

        this.accessToken = response.data.access;
        this.refreshToken = response.data.refresh;

        localStorage.setItem("token", response.data.token);
        localStorage.setItem("accessToken", this.accessToken);
        localStorage.setItem("refreshToken", this.refreshToken);
        localStorage.setItem("user_id", response.data.user_id);
        

        await this.fetchUser(); // Fetch user after login
      } catch (error) {
        console.error("Login failed:", error.response?.data || error);
      }
    },

    async fetchUser() {
      if (!this.accessToken) return;

      try {
        const response = await axios.get("http://127.0.0.1:8000/users/", {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        });

        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user:", error.response?.data || error);
      }
    },

    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
  },
});
