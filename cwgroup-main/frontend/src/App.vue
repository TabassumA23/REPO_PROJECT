<template>
    <main>
        <!--Nav bar for every page -->
        <div class="navbar">
       
                <h2>YumYelp</h2>
                <div class="nav-parts">
                      <!--Go to home page / profile page-->
                    <router-link
                        class="link"
                        :to="{name: 'ProfilePage'}"
                    >
                        ProfilePage
                    </router-link>
                      <!-- Go to find friends-->
                    <router-link
                        class="link"
                        :to="{name: 'Login'}"
                    >
                        Login
                    </router-link>

                    <!-- Logout -->
                    <a href= 'http://localhost:8000/logout/'>Log Out</a>
                </div>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>

</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>
<style scoped>
/* Navbar Styling */
nav {
  display: flex;
  justify-content: center;
  background-color: #42b983;
  padding: 10px;
  gap: 15px;
}

a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}
</style>

