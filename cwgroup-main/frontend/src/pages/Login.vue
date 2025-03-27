<template>
  <div class="auth-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label>Username</label>
        <input type="text" v-model="credentials.username" required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" v-model="credentials.password" required />
      </div>
      <button type="submit">Login</button>
      <p v-if="message">{{ message }}</p>
    </form>
    <p>Don't have an account? <router-link to="/signup">Sign up</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

// ✅ Ensure `credentials` is properly initialized as a ref object
const credentials = ref({
  username: "",
  password: "",
});

const message = ref("");

const login = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/login/", {
      username: credentials.value.username,  
      password: credentials.value.password,
    }, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    const accessToken = response.data.access;
    const refreshToken = response.data.refresh;

    if (!accessToken || !refreshToken) {
      throw new Error("No valid token received");
    }

    localStorage.setItem("accessToken", accessToken);
    localStorage.setItem("refreshToken", refreshToken);
    localStorage.setItem("user_id", response.data.user_id);

    console.log("Access Token:", accessToken);
    console.log("Refresh Token:", refreshToken);

    router.push("/profile");

  } catch (error) {
    console.error("Login failed:", error.response?.data || error);
    message.value = error.response?.data?.error || "Invalid login credentials.";
  }
};

</script>


<style scoped>
.auth-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
}
input {
  display: block;
  width: 100%;
  padding: 10px;
  margin: 5px 0;
}
button {
  padding: 10px;
  width: 100%;
  background: green;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
