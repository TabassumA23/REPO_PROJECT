<template>
  <div class="auth-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="register">
      <div>
        <label>First Name</label>
        <input type="text" v-model="user.first_name" required />
      </div>
      <div>
        <label>Last Name</label>
        <input type="text" v-model="user.last_name" required />
      </div>
      <div>
        <label>Username</label>
        <input type="text" v-model="user.username" required />
      </div>
      <div>
        <label>Email</label>
        <input type="email" v-model="user.email" required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" v-model="user.password" required />
      </div>
      <button type="submit">Sign Up</button>
      <p v-if="message">{{ message }}</p>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const user = ref({
  first_name: "",
  last_name: "",
  username: "",
  email: "",
  password: "",
});
const message = ref("");

const register = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/signup/", {
      first_name: user.value.first_name,
      last_name: user.value.last_name,
      username: user.value.username,
      email: user.value.email,
      password: user.value.password,
    }, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    message.value = response.data.message;
    router.push("/login"); // ✅ Redirect to login page
  } catch (error) {
    console.error("Signup error:", error.response?.data);
    message.value = error.response?.data?.error || "Signup failed.";
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
  background: blue;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
