import { createApp } from "vue";
import { createPinia } from "pinia";  
import App from "./App.vue";
import router from "./router";

const pinia = createPinia();  // Create Pinia instance
const app = createApp(App);

app.use(pinia);  // Register Pinia before using any store
app.use(router);
app.mount("#app");
