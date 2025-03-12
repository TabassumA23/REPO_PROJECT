import { createRouter, createWebHistory } from "vue-router";
import Login from "../pages/Login.vue";  
import Signup from "../pages/Signup.vue";
import ProfilePage from "../pages/ProfilePage.vue";
import ReservationsPage from "../pages/ReservationsPage.vue";
import WishlistPage from "../pages/WishlistPage.vue";
import ReviewsPage from "../pages/ReviewsPage.vue";
import RecommendationsPage from "../pages/RecommendationsPage.vue";

const routes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", name: "Signup", component: Signup },
  { path: "/profile", name: "ProfilePage", component: ProfilePage, meta: { requiresAuth: true } },
  {path: "/reservations", name: "Reservations", component: ReservationsPage },
  { path: "/wishlist", name: "Wishlist", component: WishlistPage },
  { path: "/reviews", name: "Reviews", component: ReviewsPage },
  { path: "/recommendations", name: "Recommendations", component: RecommendationsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
