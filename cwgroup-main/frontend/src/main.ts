import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

const pinia = createPinia(); // ✅ Initialize Pinia

const app = createApp(App);
app.use(pinia); // ✅ Use Pinia globally
app.use(router);
app.mount("#app");
